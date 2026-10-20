<div align="center">

# game-feel-ui

**Tactile Game Physics, Micro-Interactions, and Procedural Audio for Web & Mobile UI**

[![Live Playground](https://img.shields.io/badge/▶_Live_Interactive_Playground-eduuf.github.io%2Fgame--feel--ui-ffffff?style=for-the-badge&logoColor=black)](https://eduuf.github.io/game-feel-ui/)

[![CI Validation](https://github.com/EduuF/game-feel-ui/actions/workflows/ci.yml/badge.svg)](https://github.com/EduuF/game-feel-ui/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Mechanics](https://img.shields.io/badge/Mechanics-39-22c55e.svg)](./data/mechanics.csv)
[![Stacks](https://img.shields.io/badge/Stacks-11-38bdf8.svg)](./data/stacks/)
[![External Audio Assets](https://img.shields.io/badge/Audio_Assets-0_KB_(Web_Audio_API)-f59e0b.svg)](./references/procedural-web-audio.md)

**English** · [Português (PT-BR)](./README.pt-BR.md) · [**Live Interactive Demo ↗**](https://eduuf.github.io/game-feel-ui/)

</div>

---

## ▶ Try the Interactive Specimens First

Experience **Standard Linear UI vs. Game Feel UI** side-by-side in your browser (with live spring telemetry and zero-asset Web Audio synthesis):

👉 **[https://eduuf.github.io/game-feel-ui/](https://eduuf.github.io/game-feel-ui/)**

---

## Quick Install

Install across **Claude Code**, **Cursor**, **Windsurf**, or any agent supporting the `skills` standard:

```bash
npx skills add EduuF/game-feel-ui
```

<details>
<summary><strong>Manual Installation (Claude Code Local / Global)</strong></summary>

```bash
# Project-scoped skill
git clone https://github.com/EduuF/game-feel-ui.git .claude/skills/game-feel-ui

# Or global skill (available across all repositories)
git clone https://github.com/EduuF/game-feel-ui.git ~/.claude/skills/game-feel-ui
```
</details>

---

## Why `game-feel-ui`?

Game developers spend months tuning the first **50ms–150ms** of player input—using techniques coined by Steve Swink (*Game Feel*) and Martin Jonasson & Petri Purho (*Juice it or lose it*) so virtual objects feel like they have mass, tension, and physical momentum.

Most web applications feel "dead" because clicks trigger instant state swaps or linear CSS transitions (`ease-in-out`) with zero anticipation, zero kinetic recoil, and punishing hover/click boundaries.

`game-feel-ui` gives coding agents a deterministic **BM25 search engine**, **static codebase auditor**, and **39 game-feel mechanics** translated into production UI patterns:

| Game Dev Technique | What It Does in Games | Web & Mobile UI Translation |
| :--- | :--- | :--- |
| **Anticipation** | Character crouches or charges wand before firing. | **Tactile Compression (`scale(0.95)`)** on `pointerdown` before action release on `pointerup`. |
| **Hitstop / Freeze Frames** | Screen freezes for 3–5 frames on sword impact to convey weight. | **Pre-Reward Micro-Pause (60–90ms)** at peak compression on hero actions before expanding into success state. |
| **Squash & Stretch** | Projectile elongates at high velocity and flattens on impact. | **Spring Overshoot (`cubic-bezier(0.34, 1.56, 0.64, 1)`)**: modals, toggles, and badges overshoot 3–5% and settle. |
| **Coyote Time & Input Buffering** | Player can still jump 120ms after walking off a ledge. | **Invisible Forgiveness**: 160ms hover grace period on dropdowns, expanded hit-slop, and optimistic UI with undo. |
| **Hold-to-Commit Tension** | Charging a heavy attack with rising pitch and tremor. | **Modal-Free Destructive Actions**: holding a "Delete" button fills a tension bar with rising pitch and reversible decay on release. |
| **Pitch Escalation** | Collecting coins in sequence raises the musical note each time. | **Combo Checklists & Kanban Drops**: consecutive completions ascend `+2 semitones` (`f0 * 2^(n/12)`) via Web Audio API. |
| **Recoil & Knockback** | Attacker steps back; target shakes on hit. | **Damped Error Shake (`±6px → 0px`)** on invalid inputs and elastic neighbor push when list items insert/remove. |

---

## Usage in Claude Code & Cursor

Once installed, the agent automatically activates `game-feel-ui` when you ask to polish, audit, or design interactive components.

### Example Prompts

```text
"Audit our dashboard components with game-feel-ui and fix the top 3 dead interactions."
```

```text
"Replace our confirmation modal on the Delete API Key button with a Game Feel hold-to-commit interaction."
```

```text
"Add subtle tactile physics, Coyote Time hover forgiveness, and optional procedural Web Audio ticks to our Kanban board."
```

### CLI Tools (Deterministic Search, Audit & Blueprint)

The skill ships with a zero-dependency Python 3 CLI (`scripts/search.py`) used by the agent:

```bash
# 1. Audit an existing codebase (returns a 0-100 Juice Score + file:line fixes)
python scripts/search.py --audit ./src

# 2. Generate a calibrated Game-Feel Blueprint with the 3 Dials
python scripts/search.py "b2b saas kanban" --blueprint --juice 5 --forgiveness 8 --audio 3

# 3. Persist the calibrated blueprint to game-feel-system/MASTER.md
python scripts/search.py "fintech checkout" --blueprint --juice 4 --forgiveness 9 --audio 2 --persist -p "CheckoutApp"

# 4. Query specific domains or framework stacks
python scripts/search.py "destructive hold button" --domaincomponent
python scripts/search.py "spring press" --stack framer-motion
```

---

## The 3 Calibration Dials

A high-frequency B2B SaaS table cannot animate like an arcade game. `game-feel-ui` enforces the **Frequency vs. Intensity Matrix** through three orthogonal dials:

- **`--juice` (`1–10`)**: Controls visual kinematics (`--gf-press-scale`, `--gf-overshoot-scale`, `--gf-spring-stiffness`, `--gf-hitstop-ms`).
- **`--forgiveness` (`1–10`)**: Controls invisible UX ergonomics (`--gf-coyote-grace-ms`, `--gf-hit-slop-px`, `--gf-undo-window-ms`). Recommended at **`7–9`** for all productivity apps.
- **`--audio` (`0–10`)**: Controls procedural Web Audio synthesis gain (`--gf-audio-max-gain`) and haptic pulse intensity.

---

## Catalog Overview

| Dataset | Count | Description |
| :--- | :---: | :--- |
| [`data/mechanics.csv`](./data/mechanics.csv) | **39** | Core Game Feel mechanics across 6 categories (*Anticipation*, *Impact*, *Spring*, *Forgiveness*, *Spatial*, *Progression*) |
| [`data/components.csv`](./data/components.csv) | **23** | UI component recipes with **L1 Subtle**, **L2 Balanced**, and **L3 Juicy** tiers |
| [`data/audio-haptics.csv`](./data/audio-haptics.csv) | **11** | Zero-asset Web Audio API synthesizer recipes + `navigator.vibrate` patterns |
| [`data/physics-curves.csv`](./data/physics-curves.csv) | **7** | CSS `linear()`, `cubic-bezier`, and spring stiffness/damping/mass presets |
| [`data/app-profiles.csv`](./data/app-profiles.csv) | **8** | Default dial calibrations by product vertical (B2B SaaS, Fintech, EdTech, DevTools, E-Commerce, AI Chat, Consumer, Creative) |
| [`data/anti-patterns.csv`](./data/anti-patterns.csv) | **8** | Performance & UX guardrails (`prefers-reduced-motion`, 60fps compositor properties, audio fatigue) |
| [`data/stacks/*.csv`](./data/stacks/) | **11** | Framework recipes: `react`, `nextjs`, `framer-motion`, `html-tailwind`, `css-waapi`, `gsap`, `shadcn`, `vue`, `svelte`, `react-native`, `flutter` |

---

## Validation & Tests

```bash
# Validate all CSV schemas, cross-references, and catalog counts
python scripts/validate_data.py

# Run the unit test suite
python scripts/tests/test_game_feel.py
```

---

## License

MIT © [Eduardo Fiuza](https://github.com/EduuF)
