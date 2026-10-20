#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Feel UI Codebase Auditor & Opportunity Scanner.
Scans a frontend codebase (React, Next.js, Vue, Svelte, Tailwind, CSS, Flutter, RN)
to evaluate existing micro-interactions, detect "dry" UI controls and anti-patterns,
calculate a Game Feel Readiness Score (0-100), and output file:line opportunities
mapped to concrete Game Dev UI mechanics.
"""

import json
import os
import re
from pathlib import Path

IGNORE_DIRS = {
    "node_modules", ".git", ".next", "dist", "build", "out", ".nuxt",
    ".svelte-kit", "coverage", "__pycache__", ".venv", "venv", "vendor",
    ".turbo", ".cache", "game-feel"
}

UI_EXTENSIONS = {".tsx", ".jsx", ".vue", ".svelte", ".html", ".css", ".scss", ".dart"}

# Regex detectors for interactive elements and Game Feel patterns
RE_BUTTON = re.compile(r"<(button|Button|motion\.button|Pressable)\b([^>]*)", re.DOTALL)
RE_ACTIVE_PRESS = re.compile(r"active:scale|whileTap|:active\b|onPressIn|scale\(|--gf-press-scale")
RE_TRANSITION_ALL = re.compile(r"\btransition-all\b|transition:\s*all\b")
RE_LAYOUT_THRASH = re.compile(r"transition-\[(?:[^\]]*\b(?:width|height|top|left|margin|padding)\b[^\]]*)\]|@keyframes[^{]+\{[^}]*\b(?:width|height|top|left|margin)\s*:", re.DOTALL)
RE_REDUCED_MOTION = re.compile(r"prefers-reduced-motion|motion-reduce:|useReducedMotion|reducedMotion")
RE_TABULAR_NUMS = re.compile(r"tabular-nums|font-variant-numeric:\s*tabular-nums")
RE_DYNAMIC_NUM = re.compile(r"\$\{[a-zA-Z0-9_.]*(?:count|total|price|score|balance|amount|percent|progress)[a-zA-Z0-9_.]*\}|\{[a-zA-Z0-9_.]*(?:count|total|price|score|balance|amount|percent)[a-zA-Z0-9_.]*\}", re.IGNORECASE)
RE_HOVER_LEAVE_TRAP = re.compile(r"on(?:Mouse|Pointer)Leave=\{\s*\(\)\s*=>\s*set[A-Z][a-zA-Z0-9_]*\(\s*false\s*\)\s*\}")
RE_POINTER_STATE_THRASH = re.compile(r"on(?:Mouse|Pointer)Move=\{\s*\(?[a-zA-Z0-9_,\s]*\)?\s*=>\s*set[A-Z][a-zA-Z0-9_]*\(")
RE_MODAL_DIALOG = re.compile(r"<(Dialog|Modal|Drawer|Sheet|Popover|DropdownMenu|Command)\b")
RE_CHECKBOX_TOGGLE = re.compile(r"type=[\"']checkbox[\"']|<(Checkbox|Switch|Toggle)\b")
RE_DRAGGABLE = re.compile(r"\bdraggable\b|useDraggable|useSortable|<Reorder\.|onDragStart|DragDropContext")
RE_DESTRUCTIVE_BTN = re.compile(r"variant=[\"']destructive[\"']|onClick=\{[^}]*(?:delete|remove|destroy|revoke|cancel)[^}]*\}", re.IGNORECASE)
RE_COPY_CLIPBOARD = re.compile(r"navigator\.clipboard\.writeText|copyToClipboard")
RE_SPRING_CURVE = re.compile(r"cubic-bezier\(\s*0\.(?:16|22|34)|type:\s*['\"]spring['\"]|linear\(|back\.out|elastic\.out|SpringSimulation|withSpring")
RE_HITBOX_EXPAND = re.compile(r"after:-inset-|::after\s*\{[^}]*inset:\s*-")
RE_OPTIMISTIC = re.compile(r"useOptimistic|optimistic")
RE_WEB_AUDIO = re.compile(r"AudioContext|webkitAudioContext|navigator\.vibrate|Haptics\.|HapticFeedback\.")


def detect_stack(root: Path) -> dict:
    stack = []
    libraries = []
    pkg_path = root / "package.json"
    if pkg_path.exists():
        try:
            pkg = json.loads(pkg_path.read_text(encoding="utf-8", errors="ignore"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                stack.append("nextjs")
            if "react-native" in deps:
                stack.append("react-native")
            elif "react" in deps:
                stack.append("react")
            if "vue" in deps:
                stack.append("vue")
            if "svelte" in deps:
                stack.append("svelte")
            if "tailwindcss" in deps:
                stack.append("html-tailwind")
            if "framer-motion" in deps or "motion" in deps:
                stack.append("framer-motion")
                libraries.append("framer-motion")
            if "gsap" in deps or "@gsap/react" in deps:
                stack.append("gsap")
                libraries.append("gsap")
            if any(k.startswith("@radix-ui/") for k in deps):
                stack.append("shadcn")
                libraries.append("radix/shadcn")
            if "@dnd-kit/core" in deps or "react-beautiful-dnd" in deps or "@hello-pangea/dnd" in deps:
                libraries.append("dnd-kit/sortable")
            if "sonner" in deps:
                libraries.append("sonner")
        except Exception:
            pass

    if (root / "pubspec.yaml").exists():
        stack.append("flutter")

    if not stack:
        stack.append("css-waapi")

    return {"detected_stacks": stack, "detected_libraries": libraries}


def _line_number(content: str, match_pos: int) -> int:
    return content.count("\n", 0, match_pos) + 1


def audit_codebase(target_path: str, max_opportunities: int = 15) -> dict:
    root = Path(target_path).resolve()
    if not root.exists():
        return {"error": f"Path does not exist: {target_path}"}

    stack_info = detect_stack(root if root.is_dir() else root.parent)
    files_to_scan = []

    if root.is_file():
        files_to_scan.append(root)
        base_dir = root.parent
    else:
        base_dir = root
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
            for fn in filenames:
                p = Path(dirpath) / fn
                if p.suffix.lower() in UI_EXTENSIONS:
                    files_to_scan.append(p)

    stats = {
        "files_scanned": len(files_to_scan),
        "total_buttons": 0,
        "tactile_buttons": 0,
        "spring_curves_used": 0,
        "reduced_motion_guards": 0,
        "tabular_nums_used": 0,
        "dynamic_numbers_found": 0,
        "optimistic_patterns": 0,
        "hitbox_expansions": 0,
        "sensory_audio_haptics": 0,
        "anti_patterns_found": 0,
    }

    opportunities = []
    anti_patterns = []

    for filepath in files_to_scan:
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        rel_path = str(filepath.relative_to(base_dir)).replace("\\", "/")

        if RE_SPRING_CURVE.search(content):
            stats["spring_curves_used"] += len(RE_SPRING_CURVE.findall(content))
        if RE_REDUCED_MOTION.search(content):
            stats["reduced_motion_guards"] += len(RE_REDUCED_MOTION.findall(content))
        if RE_TABULAR_NUMS.search(content):
            stats["tabular_nums_used"] += len(RE_TABULAR_NUMS.findall(content))
        if RE_OPTIMISTIC.search(content):
            stats["optimistic_patterns"] += 1
        if RE_HITBOX_EXPAND.search(content):
            stats["hitbox_expansions"] += 1
        if RE_WEB_AUDIO.search(content):
            stats["sensory_audio_haptics"] += 1

        # 1. Check buttons for tactile press compression
        for m in RE_BUTTON.finditer(content):
            stats["total_buttons"] += 1
            attrs = m.group(2)
            line_no = _line_number(content, m.start())
            if RE_ACTIVE_PRESS.search(attrs) or RE_ACTIVE_PRESS.search(content):
                stats["tactile_buttons"] += 1
            else:
                opportunities.append({
                    "priority": "HIGH",
                    "tier": "High-Frequency Subliminal",
                    "location": f"{rel_path}:{line_no}",
                    "element": f"<{m.group(1)}>",
                    "mechanic_id": "anticipation-press",
                    "mechanic_name": "Tactile Press Compression",
                    "observation": "Interactive button lacks physical :active / pointerdown scale compression (feels static on click).",
                    "suggestion": "Add 50ms inward compression (`active:scale-[0.97] active:translate-y-[1px] transition-transform duration-150 ease-[cubic-bezier(0.22,1,0.36,1)]` or `whileTap={{ scale: 0.965 }}`).",
                })

        # 2. Check destructive actions for Hold-to-Confirm or Deferred Undo
        for m in RE_DESTRUCTIVE_BTN.finditer(content):
            line_no = _line_number(content, m.start())
            opportunities.append({
                "priority": "HIGH",
                "tier": "Low-Frequency Hero / Forgiveness",
                "location": f"{rel_path}:{line_no}",
                "element": "Destructive Action",
                "mechanic_id": "charge-up-anticipation / coyote-time-undo-window",
                "mechanic_name": "Hold-to-Confirm Charge-Up OR 4.5s Deferred Undo",
                "observation": "Destructive action detected. Routine deletes should use optimistic removal + 4.5s Undo toast; irreversible high-stakes deletes can use an 800ms Hold-to-Confirm charge bar.",
                "suggestion": "Replace blocking 'Are you sure?' confirm dialogs with `coyote-time-undo-window` (routine) or `charge-up-anticipation` + 80ms `hitstop-micro-pause` (high-stakes).",
            })

        # 3. Check Copy-to-Clipboard for Elastic Icon Morph
        for m in RE_COPY_CLIPBOARD.finditer(content):
            line_no = _line_number(content, m.start())
            opportunities.append({
                "priority": "MEDIUM",
                "tier": "Medium-Frequency Kinetic",
                "location": f"{rel_path}:{line_no}",
                "element": "Copy Action",
                "mechanic_id": "icon-elastic-morph",
                "mechanic_name": "Stateful SVG Icon Elastic Morph",
                "observation": "Clipboard copy action detected.",
                "suggestion": "Morph the Copy icon into an emerald Checkmark with spring overshoot (`scale(0.5) rotate(-25deg) -> scale(1) rotate(0deg)`, 220ms) + brief surface flash instead of spawning a distant corner toast.",
            })

        # 4. Check Checkboxes / Toggles for Squash & Stretch + Strikethrough Sweep
        for m in RE_CHECKBOX_TOGGLE.finditer(content):
            line_no = _line_number(content, m.start())
            opportunities.append({
                "priority": "MEDIUM",
                "tier": "Medium-Frequency Kinetic",
                "location": f"{rel_path}:{line_no}",
                "element": m.group(0)[:30],
                "mechanic_id": "squash-and-stretch-morph + strikethrough-sweep-decay",
                "mechanic_name": "Elastic Squash Pop & Strikethrough Sweep",
                "observation": "Checkbox or Toggle control found.",
                "suggestion": "Add 260ms elastic pop (`squashPop`) on check, left-to-right strikethrough sweep on task labels, and optional `pitch-escalation-combo` audio when checking multiple items in a row.",
            })

        # 5. Check Draggable / Kanban items for Physical Lift & Neighbor Knockback
        for m in RE_DRAGGABLE.finditer(content):
            line_no = _line_number(content, m.start())
            opportunities.append({
                "priority": "MEDIUM",
                "tier": "Medium-Frequency Kinetic",
                "location": f"{rel_path}:{line_no}",
                "element": "Draggable / Sortable Item",
                "mechanic_id": "drag-elevation-shadow + neighbor-knockback",
                "mechanic_name": "Physical Drag Lift, Velocity Tilt & Neighbor Knockback",
                "observation": "Drag-and-drop interaction detected.",
                "suggestion": "Lift dragged item to `scale(1.04)` with deeper shadow, tilt `±3deg` proportional to horizontal velocity, enforce a 5px drag threshold, and animate sibling slots via FLIP.",
            })

        # 6. Check Modals / Popovers / Menus for Asymmetric Enter/Exit & Coyote Time
        for m in RE_MODAL_DIALOG.finditer(content):
            line_no = _line_number(content, m.start())
            opportunities.append({
                "priority": "MEDIUM",
                "tier": "Medium-Frequency Kinetic",
                "location": f"{rel_path}:{line_no}",
                "element": f"<{m.group(1)}>",
                "mechanic_id": "asymmetric-enter-exit + follow-through-stagger",
                "mechanic_name": "Asymmetric Enter/Exit Velocity & Input Buffering",
                "observation": f"Overlay component `<{m.group(1)}>` detected.",
                "suggestion": "Ensure exit animation is 40% faster than entrance (130ms ease-in vs 230ms spring out) with immediate `pointer-events: none` on close and Frame-0 input focus on open.",
            })

        # 7. Check Dynamic Numbers without tabular-nums
        for m in RE_DYNAMIC_NUM.finditer(content):
            stats["dynamic_numbers_found"] += 1
            if not RE_TABULAR_NUMS.search(content):
                line_no = _line_number(content, m.start())
                opportunities.append({
                    "priority": "MEDIUM",
                    "tier": "Medium-Frequency Kinetic",
                    "location": f"{rel_path}:{line_no}",
                    "element": m.group(0),
                    "mechanic_id": "odometer-number-roll",
                    "mechanic_name": "Tabular Numeric Stability & Odometer Roll",
                    "observation": f"Dynamic number `{m.group(0)}` rendered in a file without `tabular-nums`.",
                    "suggestion": "Add `tabular-nums` (`font-variant-numeric: tabular-nums`) to prevent horizontal jitter when digits change, and consider a vertical odometer roll for key KPIs/prices.",
                })

        # 8. Check Anti-Patterns: Hover Leave Trap (Zero Coyote Time)
        for m in RE_HOVER_LEAVE_TRAP.finditer(content):
            stats["anti_patterns_found"] += 1
            line_no = _line_number(content, m.start())
            anti_patterns.append({
                "severity": "HIGH",
                "anti_pattern_id": "zero-coyote-hover-trap",
                "location": f"{rel_path}:{line_no}",
                "code": m.group(0),
                "issue": "Instant `setOpen(false)` on pointer/mouse leave without a Coyote Time grace period causes menus/popovers to snap shut when crossing diagonal gaps.",
                "fix": "Use a 150ms grace timeout on `onPointerLeave` that is cleared on `onPointerEnter` (`coyote-time-hover-grace`).",
            })

        # 9. Check Anti-Patterns: React State Thrashing on PointerMove
        for m in RE_POINTER_STATE_THRASH.finditer(content):
            stats["anti_patterns_found"] += 1
            line_no = _line_number(content, m.start())
            anti_patterns.append({
                "severity": "CRITICAL",
                "anti_pattern_id": "pointermove-state-thrash",
                "location": f"{rel_path}:{line_no}",
                "code": m.group(0),
                "issue": "Calling React `setState` directly inside `onMouseMove`/`onPointerMove` triggers 60-120 full component re-renders per second.",
                "fix": "Update CSS variables (`ref.current.style.setProperty('--x', ...)`) or Framer Motion `useMotionValue` outside the React render cycle.",
            })

        # 10. Check Anti-Patterns: transition-all or layout-thrashing properties
        for m in RE_TRANSITION_ALL.finditer(content):
            stats["anti_patterns_found"] += 1
            line_no = _line_number(content, m.start())
            anti_patterns.append({
                "severity": "MEDIUM",
                "anti_pattern_id": "layout-thrashing-juice",
                "location": f"{rel_path}:{line_no}",
                "code": m.group(0),
                "issue": "`transition-all` animates layout properties (width/height/padding/margin) alongside transform, causing unintended layout sluggishness.",
                "fix": "Scope transitions explicitly to compositor properties: `transition-transform` or `transition-[transform,opacity,background-color]`.",
            })

    # Calculate 5 Sub-Scores & Overall Game Feel Score (0-100)
    btn_ratio = (stats["tactile_buttons"] / stats["total_buttons"]) if stats["total_buttons"] > 0 else 0.5
    tactile_score = min(25, int(btn_ratio * 15) + min(10, stats["spring_curves_used"] * 3))
    forgiveness_score = min(25, 8 + min(9, stats["optimistic_patterns"] * 5) + min(8, stats["hitbox_expansions"] * 4))
    sensory_score = min(20, 6 + min(8, stats["tabular_nums_used"] * 3) + min(6, stats["sensory_audio_haptics"] * 6))
    a11y_perf_score = max(0, min(30, 20 + min(10, stats["reduced_motion_guards"] * 5) - stats["anti_patterns_found"] * 3))
    total_score = max(5, min(100, tactile_score + forgiveness_score + sensory_score + a11y_perf_score))

    # Deduplicate and cap opportunities
    seen_locs = set()
    deduped_opps = []
    # Sort HIGH priority first
    for opp in sorted(opportunities, key=lambda x: 0 if x["priority"] == "HIGH" else 1):
        key = (opp["location"], opp["mechanic_id"])
        if key not in seen_locs:
            seen_locs.add(key)
            deduped_opps.append(opp)
        if len(deduped_opps) >= max_opportunities:
            break

    return {
        "target": str(root),
        "stack_info": stack_info,
        "score": {
            "total": total_score,
            "tactile_physics": f"{tactile_score}/25",
            "forgiveness_coyote": f"{forgiveness_score}/25",
            "sensory_numeric": f"{sensory_score}/20",
            "compositor_a11y": f"{a11y_perf_score}/30",
        },
        "stats": stats,
        "anti_patterns": anti_patterns[:10],
        "opportunities": deduped_opps,
    }


def format_audit_report(report: dict) -> str:
    if "error" in report:
        return f"Error: {report['error']}"

    sc = report["score"]
    st = report["stats"]
    stk = ", ".join(report["stack_info"]["detected_stacks"]) or "generic"
    libs = ", ".join(report["stack_info"]["detected_libraries"]) or "none detected"

    out = [
        "======================================================================================",
        f"🎮 GAME FEEL UI — CODEBASE AUDIT & OPPORTUNITY REPORT",
        "======================================================================================",
        f"Target Path:        {report['target']}",
        f"Detected Stack:     {stk} (Libraries: {libs})",
        f"Files Scanned:      {st['files_scanned']} UI files",
        f"OVERALL JUICE SCORE: {sc['total']}/100",
        f"  ├─ Tactile & Spring Physics:     {sc['tactile_physics']} (Buttons w/ press feel: {st['tactile_buttons']}/{st['total_buttons']}, Spring curves: {st['spring_curves_used']})",
        f"  ├─ Forgiveness (Coyote/Buffer):  {sc['forgiveness_coyote']} (Optimistic UI: {st['optimistic_patterns']}, Hitbox expansions: {st['hitbox_expansions']})",
        f"  ├─ Sensory & Numeric Polish:     {sc['sensory_numeric']} (tabular-nums: {st['tabular_nums_used']}, Audio/Haptics: {st['sensory_audio_haptics']})",
        f"  └─ Compositor & A11y Safety:     {sc['compositor_a11y']} (Reduced-motion guards: {st['reduced_motion_guards']}, Anti-patterns: {st['anti_patterns_found']})",
        "",
    ]

    if report["anti_patterns"]:
        out.append("## ⚠️  DETECTED GAME-FEEL ANTI-PATTERNS (FIX FIRST)")
        for i, ap in enumerate(report["anti_patterns"], 1):
            out.append(f"{i}. [{ap['severity']}] `{ap['location']}` — **{ap['anti_pattern_id']}**")
            out.append(f"   - **Issue:** {ap['issue']}")
            out.append(f"   - **Fix:** {ap['fix']}")
        out.append("")

    if report["opportunities"]:
        out.append("## ✨ TOP GAME FEEL OPPORTUNITIES (FILE : LINE)")
        for i, opp in enumerate(report["opportunities"], 1):
            out.append(
                f"{i}. [{opp['priority']} | {opp['tier']}] `{opp['location']}` ({opp['element']})"
            )
            out.append(f"   - **Technique:** `{opp['mechanic_id']}` ({opp['mechanic_name']})")
            out.append(f"   - **Why:** {opp['observation']}")
            out.append(f"   - **How to Apply:** {opp['suggestion']}")
        out.append("")
    else:
        out.append("## ✨ No static opportunities flagged — run a `--blueprint` query to design Hero Moments!")

    return "\n".join(out)
