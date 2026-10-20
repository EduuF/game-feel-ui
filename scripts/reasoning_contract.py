#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Reasoning Contract for game-feel-ui.
Maps user query signals and audited codebase features (e.g., if_destructive,
if_kanban, if_realtime, if_ai_streaming, if_checkout, if_keyboard_first,
if_gamified, if_data_heavy, if_onboarding, if_forms) to exact Game Feel
mechanics, component recipes, and sensory dial adjustments without polluting
the LLM context window.
"""

import json
import re

CONDITION_SIGNALS = {
    "if_destructive": ("delete", "remove", "revoke", "destroy", "cancel subscription", "danger", "destructive", "trash"),
    "if_kanban_drag": ("kanban", "drag", "drop", "sortable", "reorder", "board", "dnd", "column"),
    "if_realtime_live": ("realtime", "real-time", "websocket", "live", "stream", "ticker", "polling", "webhook"),
    "if_ai_streaming": ("ai", "llm", "prompt", "copilot", "chat", "generate", "streaming", "token", "agent"),
    "if_checkout_payment": ("checkout", "payment", "pay", "cart", "stripe", "purchase", "order", "invoice", "wallet"),
    "if_keyboard_first": ("cmd+k", "cmdk", "shortcut", "hotkey", "command palette", "keyboard", "vim", "raycast", "linear"),
    "if_gamified": ("streak", "xp", "badge", "level", "quiz", "habit", "reward", "milestone", "achievement", "onboarding"),
    "if_data_heavy": ("table", "datagrid", "chart", "analytics", "metrics", "kpi", "dashboard", "logs", "timeseries"),
    "if_forms_validation": ("form", "input", "login", "signup", "auth", "otp", "password", "validation", "submit"),
    "if_navigation_menus": ("dropdown", "submenu", "popover", "tooltip", "mega menu", "navbar", "sidebar", "tabs"),
    "if_media_scrubber": ("slider", "scrubber", "timeline", "audio player", "video", "volume", "range", "progress"),
    "if_copy_share": ("copy", "clipboard", "share", "snippet", "code block", "invite link"),
}

CONDITION_PATTERNS = {
    cond: tuple(re.compile(r"(?<!\w)" + re.escape(sig) + r"(?!\w)", re.IGNORECASE) for sig in sigs)
    for cond, sigs in CONDITION_SIGNALS.items()
}

# Deterministic actions triggered when a condition is detected in the query or codebase
RULE_ACTIONS = {
    "if_destructive": {
        "mechanics": ["charge-up-anticipation", "coyote-time-undo-window", "hitstop-micro-pause"],
        "components": ["destructive-hold-button", "toast-notification-stack"],
        "audio": ["charge-tension-riser", "heavy-drop-thud"],
        "constraint": "Distinguish routine deletes (use 0ms optimistic collapse + 4.5s Undo toast) from irreversible destructive actions (use 800ms hold-to-confirm charge bar + 85ms hitstop).",
    },
    "if_kanban_drag": {
        "mechanics": ["drag-elevation-shadow", "neighbor-knockback", "detent-haptic-tick", "viscous-rubber-band", "ghost-slot-magnet"],
        "components": ["kanban-draggable-card"],
        "audio": ["heavy-drop-thud", "ratchet-detent-tick"],
        "constraint": "Enforce a 5px Euclidean drag threshold before pickup; lift dragged card to scale(1.04) with velocity tilt (±3deg) and animate sibling displacement via FLIP.",
    },
    "if_realtime_live": {
        "mechanics": ["impact-flash-frame", "odometer-number-roll", "live-pulse-beacon"],
        "components": ["kpi-metric-counter", "data-table-row-action"],
        "audio": ["ratchet-detent-tick"],
        "constraint": "Enforce font-variant-numeric: tabular-nums on all live counters and flash updated rows with a 50ms->500ms decaying surface tint.",
    },
    "if_ai_streaming": {
        "mechanics": ["recoil-kickback", "border-energy-beam", "skeleton-breathing-sheen", "input-buffering-queue", "scroll-anchor-forgiveness"],
        "components": ["ai-streaming-composer", "copy-to-clipboard"],
        "audio": ["tactile-switch-click", "glassy-completion-ping"],
        "constraint": "Never hijack user scroll during token streaming if the user has scrolled up >40px from the bottom (Scroll Anchor Forgiveness).",
    },
    "if_checkout_payment": {
        "mechanics": ["hitstop-micro-pause", "odometer-number-roll", "specular-shimmer-sweep", "morphing-submit-button"],
        "components": ["primary-cta-button", "kpi-metric-counter", "pricing-bento-card"],
        "audio": ["hero-triad-chime", "tactile-switch-click"],
        "constraint": "Morph the checkout button seamlessly from Idle -> Processing -> 85ms Hitstop -> Checkmark Confirmed without shifting layout width.",
    },
    "if_keyboard_first": {
        "mechanics": ["keycap-shortcut-depression", "input-buffering-queue", "focus-ring-spring-glide", "shared-element-flip-morph"],
        "components": ["command-palette-cmdk", "dropdown-popover-menu"],
        "audio": ["wooden-keycap-thunk", "tactile-switch-click"],
        "constraint": "Focus inputs at Frame 0 of mount so fast typing after Cmd+K never drops initial characters.",
    },
    "if_gamified": {
        "mechanics": ["pitch-escalation-combo", "particle-micro-burst", "hitstop-micro-pause", "squash-and-stretch-morph", "harmonic-chord-confirm"],
        "components": ["onboarding-progress-checklist", "checkbox-task-item", "like-reaction-bookmark"],
        "audio": ["combo-semitone-ramp", "hero-triad-chime", "soft-bubble-pop"],
        "constraint": "Keep celebration sequences 100% interruptible so power users can click 'Continue' without waiting for particles to finish.",
    },
    "if_data_heavy": {
        "mechanics": ["odometer-number-roll", "spring-tether-tooltip", "impact-flash-frame", "coyote-time-hover-grace"],
        "components": ["kpi-metric-counter", "data-table-row-action", "filter-pill-bar"],
        "audio": ["ratchet-detent-tick"],
        "constraint": "Cap juice intensity at <=4/10 on dense data tables; avoid scale overshoot on table rows and prioritize tabular-nums + instant hover crosshairs.",
    },
    "if_forms_validation": {
        "mechanics": ["trauma-error-shake", "focus-ring-spring-glide", "reward-early-validate-late", "otp-auto-advance-pop"],
        "components": ["form-input-validation", "otp-pin-input", "primary-cta-button"],
        "audio": ["error-reject-buzz", "soft-bubble-pop"],
        "constraint": "Reward early, punish late: validate new inputs on blur, but clear error state immediately on keystroke as soon as the field becomes valid.",
    },
    "if_navigation_menus": {
        "mechanics": ["coyote-time-hover-grace", "asymmetric-enter-exit", "shared-element-flip-morph", "safe-triangle-aim"],
        "components": ["dropdown-popover-menu", "tab-segmented-control"],
        "audio": ["tactile-switch-click"],
        "constraint": "Apply 150ms Coyote Time on pointerleave and make exit animations 40% faster than entrance animations with immediate pointer-events: none.",
    },
    "if_media_scrubber": {
        "mechanics": ["detent-haptic-tick", "viscous-rubber-band", "squash-and-stretch-morph"],
        "components": ["range-slider-scrubber"],
        "audio": ["ratchet-detent-tick"],
        "constraint": "Throttle detent ticks to >=25ms intervals during fast scrubbing and expand thumb hitbox by +12px via ::after.",
    },
    "if_copy_share": {
        "mechanics": ["icon-elastic-morph", "impact-flash-frame", "anticipation-press"],
        "components": ["copy-to-clipboard"],
        "audio": ["camera-shutter-snip"],
        "constraint": "Morph the Copy icon directly into a green Checkmark at the cursor locus instead of firing a distant corner toast.",
    },
}


def evaluate_context_rules(text: str, extra_conditions: list = None) -> dict:
    """Evaluate text + audited conditions and return deterministic mechanics, components, audio, and constraints."""
    norm = str(text or "").lower()
    activated = []
    for cond, patterns in CONDITION_PATTERNS.items():
        if any(p.search(norm) for p in patterns):
            activated.append(cond)
    if extra_conditions:
        for c in extra_conditions:
            if c in RULE_ACTIONS and c not in activated:
                activated.append(c)

    mechanics = []
    components = []
    audio = []
    constraints = []

    for cond in activated:
        act = RULE_ACTIONS[cond]
        for m in act["mechanics"]:
            if m not in mechanics:
                mechanics.append(m)
        for comp in act["components"]:
            if comp not in components:
                components.append(comp)
        for aud in act["audio"]:
            if aud not in audio:
                audio.append(aud)
        if act["constraint"] not in constraints:
            constraints.append(act["constraint"])

    return {
        "activated_conditions": activated,
        "priority_mechanics": mechanics,
        "priority_components": components,
        "priority_audio": audio,
        "constraints": constraints,
    }
