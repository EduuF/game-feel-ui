#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Feel Blueprint Generator - Aggregates product profiles, mechanics,
components, physics curves, and audio recipes into a cohesive Game Feel Blueprint.
Supports --juice, --forgiveness, and --audio dials (1-10) and --persist.
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from core import DATA_DIR, search, _load_csv
from reasoning_contract import evaluate_context_rules

BOX_WIDTH = 92

DIAL_TIERS = {
    "juice": [
        (1, 3, {
            "label": "Subliminal & Crisp (Precision First)",
            "max_high_ms": "120ms",
            "max_med_ms": "200ms",
            "press_scale": "0.975",
            "curve_id": "snappy-decelerate",
        }),
        (4, 7, {
            "label": "Kinetic & Tactile (Balanced Spring Feel)",
            "max_high_ms": "150ms",
            "max_med_ms": "260ms",
            "press_scale": "0.965",
            "curve_id": "spring-subtle-overshoot",
        }),
        (8, 10, {
            "label": "Expressive & Celebratory (High-Reward Gamified)",
            "max_high_ms": "170ms",
            "max_med_ms": "320ms",
            "press_scale": "0.95",
            "curve_id": "spring-juicy-bounce",
        }),
    ],
    "forgiveness": [
        (1, 3, {"label": "Standard Hitboxes & 100ms Grace", "coyote_ms": "100ms", "hitbox_px": "4px"}),
        (4, 7, {"label": "Generous Coyote Time (150ms) & +8px Hitboxes", "coyote_ms": "150ms", "hitbox_px": "8px"}),
        (8, 10, {"label": "Maximum Assist (180ms Grace, +12px Hitbox, Magnetic Snap, 5s Undo)", "coyote_ms": "180ms", "hitbox_px": "12px"}),
    ],
    "audio": [
        (1, 3, {"label": "Silent Visual-Only + Mobile Haptics", "policy": "Haptics only (navigator.vibrate(4)); zero desktop audio"}),
        (4, 7, {"label": "Subliminal Hardware Ticks (Opt-in, <=0.04 Gain)", "policy": "10ms triangle switch clicks + combo pitch ramp on streaks"}),
        (8, 10, {"label": "Full Procedural Sensory Suite", "policy": "Switch clicks, bubble pops, combo semitone ramps, drop thuds & Hero triad chimes"}),
    ],
}


def _resolve_dial(name: str, value) -> dict:
    if value is None:
        return None
    val = max(1, min(10, int(value)))
    for lo, hi, info in DIAL_TIERS[name]:
        if lo <= val <= hi:
            return {**info, "value": val}
    return None


def generate_blueprint(
    query: str,
    project_name: str = None,
    output_format: str = "ascii",
    persist: bool = False,
    component: str = None,
    output_dir: str = None,
    juice: int = None,
    forgiveness: int = None,
    audio: int = None,
    force: bool = False,
) -> dict:
    profiles = _load_csv(DATA_DIR / "app-profiles.csv")
    mechanics_all = _load_csv(DATA_DIR / "mechanics.csv")
    mechanics_by_id = {m.get("Mechanic ID"): m for m in mechanics_all}
    curves_all = _load_csv(DATA_DIR / "physics-curves.csv")
    curves_by_id = {c.get("Curve ID"): c for c in curves_all}

    # 1. Match best App Profile
    prof_res = search(query, "profiles", max_results=1)
    matched_profile = prof_res["results"][0] if prof_res.get("results") else (profiles[0] if profiles else {})

    # Default juice dial from profile if not explicitly provided
    default_juice = 5
    budget_str = matched_profile.get("Recommended Juice Budget", "5/10")
    m_num = re.search(r"(\d+)\s*/\s*10", budget_str)
    if m_num:
        default_juice = int(m_num.group(1))

    juice_info = _resolve_dial("juice", juice if juice is not None else default_juice)
    forgive_info = _resolve_dial("forgiveness", forgiveness if forgiveness is not None else 6)
    audio_info = _resolve_dial("audio", audio if audio is not None else (7 if default_juice >= 7 else 4))

    # 2. Evaluate deterministic context rules + resolve mechanics from profile & query
    context_rules = evaluate_context_rules(query)
    rec_ids = (
        context_rules["priority_mechanics"]
        + [
            mid.strip()
            for mid in matched_profile.get("Recommended Mechanics", "").split("+")
            if mid.strip()
        ]
    )
    mech_search = search(query, "mechanics", max_results=4).get("results", [])
    selected_mechanics = []
    seen_ids = set()
    for mid in rec_ids:
        if mid in mechanics_by_id and mid not in seen_ids and len(selected_mechanics) < 6:
            selected_mechanics.append(mechanics_by_id[mid])
            seen_ids.add(mid)
    for m in mech_search:
        mid = m.get("Mechanic ID")
        if mid and mid not in seen_ids and len(selected_mechanics) < 6:
            selected_mechanics.append(m)
            seen_ids.add(mid)

    # 3. Match top Component Recipes & Audio & Physics Curve
    comp_results = search(query, "components", max_results=3).get("results", [])
    audio_results = search(query, "audio", max_results=2).get("results", [])
    primary_curve = curves_by_id.get(juice_info["curve_id"], curves_all[0] if curves_all else {})
    exit_curve = curves_by_id.get("crisp-exit-accelerate", {})

    blueprint = {
        "project_name": project_name or query.upper(),
        "query": query,
        "profile": matched_profile,
        "dials": {
            "juice": juice_info,
            "forgiveness": forgive_info,
            "audio": audio_info,
        },
        "mechanics": selected_mechanics,
        "components": comp_results,
        "audio_recipes": audio_results,
        "activated_rules": context_rules,
        "curves": {
            "primary": primary_curve,
            "exit": exit_curve,
        },
        "tokens": {
            "--gf-press-scale": juice_info["press_scale"],
            "--gf-press-duration": "55ms",
            "--gf-release-duration": juice_info["max_high_ms"],
            "--gf-ease-spring": primary_curve.get("CSS Easing / linear()", "cubic-bezier(0.22, 1, 0.36, 1)"),
            "--gf-ease-exit": exit_curve.get("CSS Easing / linear()", "cubic-bezier(0.4, 0, 1, 1)"),
            "--gf-exit-duration": "130ms",
            "--gf-coyote-grace": forgive_info["coyote_ms"],
            "--gf-hitbox-expand": f"-{forgive_info['hitbox_px']}",
        },
    }

    text = format_markdown_blueprint(blueprint) if output_format == "markdown" else format_ascii_blueprint(blueprint)

    persistence_info = None
    if persist:
        persistence_info = _persist_blueprint(blueprint, output_dir, component, force)

    return {
        "blueprint": blueprint,
        "text": text,
        "persistence": persistence_info,
    }


def _wrap_line(text: str, prefix: str, width: int) -> list:
    if not text:
        return []
    room = max(20, width - 2 - len(prefix))
    words = text.split()
    lines = []
    curr = prefix
    for w in words:
        if len(curr) + len(w) + 1 <= width - 2:
            curr += (" " if curr != prefix else "") + w
        else:
            lines.append(curr.ljust(width - 1) + "│")
            curr = prefix + w
    if curr != prefix:
        lines.append(curr.ljust(width - 1) + "│")
    return lines


def _section_sep(title: str, width: int = BOX_WIDTH) -> str:
    label = f"─── {title} "
    fill = "─" * max(1, width - len(label) - 2)
    return f"├{label}{fill}┤"


def format_ascii_blueprint(bp: dict) -> str:
    w = BOX_WIDTH - 2
    lines = []
    prof = bp["profile"]
    dials = bp["dials"]

    lines.append("╔" + "═" * w + "╗")
    hdr = f"║  🎮 GAME FEEL UI BLUEPRINT — {bp['project_name']}"
    lines.append(hdr[: BOX_WIDTH - 1].ljust(BOX_WIDTH - 1) + "║")
    lines.append("╚" + "═" * w + "╝")
    lines.append("┌" + "─" * w + "┐")

    lines.append(_section_sep("ARCHETYPE & SENSORY DIALS"))
    lines.extend(_wrap_line(f"Archetype:   {prof.get('Product Archetype', 'General Application')}", "│  ", BOX_WIDTH))
    lines.extend(_wrap_line(f"Juice Dial:  {dials['juice']['value']}/10 — {dials['juice']['label']}", "│  ", BOX_WIDTH))
    lines.extend(_wrap_line(f"Forgiveness: {dials['forgiveness']['value']}/10 — {dials['forgiveness']['label']}", "│  ", BOX_WIDTH))
    lines.extend(_wrap_line(f"Sensory/SFX: {dials['audio']['value']}/10 — {dials['audio']['label']}", "│  ", BOX_WIDTH))

    lines.append(_section_sep("FREQUENCY × INTENSITY BUDGET"))
    lines.extend(_wrap_line(f"1. High-Freq (Subliminal): {prof.get('High-Freq Tier Strategy', '')}", "│  ", BOX_WIDTH))
    lines.extend(_wrap_line(f"2. Med-Freq (Kinetic):     {prof.get('Medium-Freq Tier Strategy', '')}", "│  ", BOX_WIDTH))
    lines.extend(_wrap_line(f"3. Low-Freq (Hero Moment): {prof.get('Hero Moment Strategy', '')}", "│  ", BOX_WIDTH))

    lines.append(_section_sep("CSS DESIGN TOKENS (COPY-PASTE)"))
    for k, v in bp["tokens"].items():
        lines.extend(_wrap_line(f"{k}: {v};", "│    ", BOX_WIDTH))

    lines.append(_section_sep("CORE GAME FEEL MECHANICS TO APPLY"))
    for i, m in enumerate(bp["mechanics"][:5], 1):
        lines.extend(_wrap_line(
            f"{i}. [{m.get('Mechanic ID')}] {m.get('Mechanic Name')} ({m.get('Frequency Tier')})",
            "│  ", BOX_WIDTH
        ))
        lines.extend(_wrap_line(f"Spec: {m.get('Timing / Physics Spec', '')}", "│     ", BOX_WIDTH))

    if bp["components"]:
        lines.append(_section_sep("MATCHED COMPONENT CHOREOGRAPHY"))
        for c in bp["components"][:2]:
            lines.extend(_wrap_line(f"▸ {c.get('Component Name')} ({c.get('Component ID')})", "│  ", BOX_WIDTH))
            lines.extend(_wrap_line(f"Wind-up:     {c.get('Anticipation (Wind-up)')}", "│    ", BOX_WIDTH))
            lines.extend(_wrap_line(f"Impact:      {c.get('Impact (Activation)')}", "│    ", BOX_WIDTH))
            lines.extend(_wrap_line(f"Settle:      {c.get('Follow-Through (Settle)')}", "│    ", BOX_WIDTH))
            lines.extend(_wrap_line(f"Forgiveness: {c.get('Forgiveness (Invisible Feel)')}", "│    ", BOX_WIDTH))

    lines.append(_section_sep("ANTI-PATTERNS TO AVOID"))
    lines.extend(_wrap_line(prof.get("Avoid (Anti-Patterns)", "Avoid slot-machine fatigue and blocking animations."), "│  ⚠️  ", BOX_WIDTH))

    lines.append("└" + "─" * w + "┘")
    return "\n".join(lines)


def format_markdown_blueprint(bp: dict) -> str:
    prof = bp["profile"]
    dials = bp["dials"]
    out = [
        f"# Game Feel UI Blueprint — {bp['project_name']}",
        "",
        f"- **Product Archetype:** {prof.get('Product Archetype', 'General Application')}",
        f"- **Juice Dial:** `{dials['juice']['value']}/10` — {dials['juice']['label']}",
        f"- **Forgiveness Dial:** `{dials['forgiveness']['value']}/10` — {dials['forgiveness']['label']}",
        f"- **Audio & Haptics Dial:** `{dials['audio']['value']}/10` — {dials['audio']['label']}",
        "",
        "## 1. Frequency × Intensity Budget",
        f"- **High-Frequency (Subliminal, 50+ uses/session):** {prof.get('High-Freq Tier Strategy', '')}",
        f"- **Medium-Frequency (Kinetic, 5–30 uses/session):** {prof.get('Medium-Freq Tier Strategy', '')}",
        f"- **Low-Frequency (Hero Moments, 1–3 uses/session):** {prof.get('Hero Moment Strategy', '')}",
        "",
        "## 2. Global Game Feel CSS Tokens",
        "```css",
        ":root {",
    ]
    for k, v in bp["tokens"].items():
        out.append(f"  {k}: {v};")
    out.extend([
        "}",
        "@media (prefers-reduced-motion: reduce) {",
        "  :root {",
        "    --gf-press-scale: 1;",
        "    --gf-release-duration: 0ms;",
        "  }",
        "}",
        "```",
        "",
        "## 3. Recommended Game Feel Mechanics",
    ])
    for m in bp["mechanics"]:
        out.extend([
            f"### `{m.get('Mechanic ID')}` — {m.get('Mechanic Name')} ({m.get('Frequency Tier')})",
            f"- **Game Dev Origin:** {m.get('Game Dev Origin')}",
            f"- **UI Equivalent:** {m.get('UI Equivalent')}",
            f"- **Timing / Physics Spec:** {m.get('Timing / Physics Spec')}",
            f"- **Reduced Motion Fallback:** {m.get('Reduced Motion Fallback')}",
            "```css",
            m.get("CSS / JS Snippet", ""),
            "```",
            "",
        ])

    if bp["components"]:
        out.append("## 4. Component Choreography Recipes")
        for c in bp["components"]:
            out.extend([
                f"### {c.get('Component Name')} (`{c.get('Component ID')}`)",
                f"- **Anticipation (Wind-up):** {c.get('Anticipation (Wind-up)')}",
                f"- **Impact (Activation):** {c.get('Impact (Activation)')}",
                f"- **Follow-Through (Settle):** {c.get('Follow-Through (Settle)')}",
                f"- **Forgiveness (Invisible Feel):** {c.get('Forgiveness (Invisible Feel)')}",
                f"- **Audio & Haptics:** {c.get('Audio & Haptic Pairing')}",
                f"- **Code Recipe:** `{c.get('Code Recipe')}`",
                "",
            ])

    out.extend([
        "## 5. Anti-Patterns to Avoid",
        f"- {prof.get('Avoid (Anti-Patterns)', '')}",
    ])
    return "\n".join(out)


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "project").lower()).strip("-")
    return slug or "project"


def _persist_blueprint(bp: dict, output_dir: str, component: str, force: bool) -> dict:
    base_dir = Path(output_dir).resolve() if output_dir else Path.cwd()
    slug = _slugify(bp["project_name"])
    gf_dir = base_dir / "game-feel" / slug
    comp_dir = gf_dir / "components"
    master_file = gf_dir / "MASTER.md"

    created = []
    if master_file.exists() and not force and not component:
        return {
            "status": "skipped_exists",
            "design_system_dir": str(gf_dir),
            "message": f"MASTER.md already exists at {master_file}. Pass --force to overwrite.",
            "created_files": [],
        }

    gf_dir.mkdir(parents=True, exist_ok=True)
    comp_dir.mkdir(parents=True, exist_ok=True)

    if not master_file.exists() or force:
        master_file.write_text(format_markdown_blueprint(bp), encoding="utf-8")
        created.append(str(master_file))

    if component:
        comp_slug = _slugify(component)
        comp_file = comp_dir / f"{comp_slug}.md"
        if not comp_file.exists() or force:
            comp_search = search(component, "components", max_results=2).get("results", [])
            lines = [
                f"# Component Game Feel Override — {component}",
                f"Generated: {datetime.now().strftime('%Y-%m-%d')}",
                "",
            ]
            for c in comp_search:
                lines.extend([
                    f"## {c.get('Component Name')} (`{c.get('Component ID')}`)",
                    f"- **Frequency Tier:** {c.get('Frequency Tier')}",
                    f"- **Anticipation:** {c.get('Anticipation (Wind-up)')}",
                    f"- **Impact:** {c.get('Impact (Activation)')}",
                    f"- **Follow-Through:** {c.get('Follow-Through (Settle)')}",
                    f"- **Forgiveness:** {c.get('Forgiveness (Invisible Feel)')}",
                    f"- **Audio & Haptics:** {c.get('Audio & Haptic Pairing')}",
                    f"- **Code Recipe:** `{c.get('Code Recipe')}`",
                    f"- **Avoid:** {c.get('Avoid')}",
                    "",
                ])
            comp_file.write_text("\n".join(lines), encoding="utf-8")
            created.append(str(comp_file))

    return {
        "status": "success",
        "design_system_dir": str(gf_dir),
        "created_files": created,
    }
