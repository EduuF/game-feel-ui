<div align="center">

<a href="https://e-fiuza.github.io/game-feel-ui/">
  <img src="./docs/assets/hero-banner.svg" alt="game-feel-ui — The physics of the first 120 milliseconds" width="100%" />
</a>

<br />

<p align="center">
  <a href="https://e-fiuza.github.io/game-feel-ui/"><strong>▶ Live Interactive Demos</strong></a>
  &nbsp;·&nbsp;
  <a href="https://e-fiuza.github.io/game-feel-ui/install.html"><strong>📖 Install &amp; Usage Tutorial</strong></a>
  &nbsp;·&nbsp;
  <a href="#install"><strong>Quick Install</strong></a>
  &nbsp;·&nbsp;
  <a href="#three-workflows"><strong>Three Workflows</strong></a>
  &nbsp;·&nbsp;
  <a href="#from-game-engine-to-the-dom"><strong>39 Mechanics</strong></a>
  &nbsp;·&nbsp;
  <a href="./README.pt-BR.md"><strong>Português (PT-BR)</strong></a>
</p>

<p align="center">
  <a href="https://e-fiuza.github.io/game-feel-ui/"><img src="https://img.shields.io/badge/Live_Sandbox-e--fiuza.github.io%2Fgame--feel--ui-ff5722?style=flat-square" alt="Live Interactive Sandbox" /></a>
  <a href="https://github.com/e-fiuza/game-feel-ui/actions/workflows/ci.yml"><img src="https://github.com/e-fiuza/game-feel-ui/actions/workflows/ci.yml/badge.svg?style=flat-square" alt="CI Validation" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-18181b?style=flat-square" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/works_with-Claude_Code_%2B_Cursor_%2B_Codex_%2B_Windsurf-18181b?style=flat-square" alt="Works with Claude Code, Cursor, Codex, Windsurf" />
  <img src="https://img.shields.io/badge/audio_assets-0_KB_(Web_Audio_API)-10b981?style=flat-square" alt="0 KB Audio Assets" />
</p>

</div>

---

**AI-generated frontends work, but they often feel lifeless—pages look static, clicks have no weight, and interactions swap state in `0ms` or behind a generic `transition: all 0.3s ease`.**

**`game-feel-ui`** is an open-source skill for **Claude Code**, **Cursor**, **Codex**, **Windsurf**, and **Gemini CLI** that spots dull, flat spots in your interface and makes your frontend feel **dynamic, fluid, tactile, and attractive**—using subtle, proven interaction tricks from game development.

Game studios spend months tuning the first **50ms–120ms** of user input—applying principles coined by Steve Swink (*Game Feel*) and Martin Jonasson & Petri Purho (*Juice it or lose it*) so virtual controls carry real mass, tension, and momentum. This skill brings **39 deterministic mechanics** (*Squash & Stretch, Hitstop, Spring Overshoot*), **invisible UX forgiveness** (*Coyote Time hover grace, Hold-to-Commit*), and **zero-asset Web Audio synthesis** to **11 modern web and mobile stacks** without turning serious software into distracting gamification.

> [!TIP]
> **Want to feel the difference before reading?** Open the **[Live Interactive Showcase ↗](https://e-fiuza.github.io/game-feel-ui/)** to test the **0.25x Slow-Motion Comparison**, interact with **12 side-by-side Standard UI vs. Game Feel UI demos**, and hear the **0 KB Web Audio synthesizer** live in your browser.

---

## Install

```bash
npx skills add e-fiuza/game-feel-ui
```

> 📖 **Need a step-by-step walkthrough or ready-to-copy prompts?** Read the **[Interactive Installation & Prompting Tutorial ↗](https://e-fiuza.github.io/game-feel-ui/install.html)**.

<details>
<summary><strong>Claude Code Plugin Marketplace</strong></summary>

Run inside a Claude Code session:

```text
/plugin marketplace add e-fiuza/game-feel-ui
/plugin install game-feel-ui
```
</details>

<details>
<summary><strong>Manual Clone (Project or Global Scope)</strong></summary>

```bash
# Project-scoped skill
git clone https://github.com/e-fiuza/game-feel-ui.git .claude/skills/game-feel-ui

# Global skill across all repositories
git clone https://github.com/e-fiuza/game-feel-ui.git ~/.claude/skills/game-feel-ui
```
</details>

---

## Three Workflows

Describe the outcome you want in natural language, or trigger a specific deterministic workflow:

| Mode | You type, for example | You get |
| :--- | :--- | :--- |
| **`01 · Component Polish`**<br />*Single interaction or screen* | `"Make our dashboard feel more dynamic and fluid—upgrade our primary buttons, toggles, and dropdowns with game-feel-ui."` | Queries 39 mechanics and 11 stack guides to deliver compositor-safe (`transform`/`opacity`) spring physics, preload compression, 160ms Coyote Time hover forgiveness, and `prefers-reduced-motion` fallbacks. |
| **`02 · Codebase Audit`**<br />*Static repository scanner* | `"Audit our dashboard components with game-feel-ui and fix the top 3 dead interactions."` | Runs `scripts/search.py --audit`, calculates a **0–100 Juice Score**, pinpoints dead clicks, blocking `window.confirm()` dialogs, and layout-thrashing animations by `file:line`, and patches them. |
| **`03 · System Blueprint`**<br />*Calibrated design tokens* | `"Generate a B2B SaaS Game Feel blueprint calibrated with juice 5, forgiveness 8, audio 3 and persist it."` | Runs `scripts/search.py --blueprint --persist`, calibrates CSS Custom Properties (`--gf-press-scale`, `--gf-hitstop-ms`, `--gf-coyote-grace-ms`), and writes the contract to `game-feel-system/MASTER.md`. |

---

## From Game Engine to the DOM

Every classic game-feel technique maps to a concrete, high-craft UI engineering pattern:

| Game Dev Mechanic | What It Does in Games | Web & Mobile UI Translation |
| :--- | :--- | :--- |
| **Anticipation (`M01`)** | Character crouches or charges wand before firing. | **Tactile Preload (`scale(0.94)`)** on `pointerdown` storing elastic potential energy before `pointerup`. |
| **Hitstop / Freeze Frames (`M04`)** | Screen freezes for 3–5 frames on sword impact to convey weight. | **Pre-Reward Micro-Pause (60–85ms)** at peak compression on primary CTAs before rebounding into success state. |
| **Squash & Stretch (`M08/M09`)** | Projectile elongates at high speed and flattens on impact. | **Spring Overshoot & Thumb Morph**: switch thumbs elongate `scaleX(1.25)` mid-travel and settle with `cubic-bezier(0.34, 1.56, 0.64, 1)`. |
| **Coyote Time (`M15–M19`)** | Player can still jump 120ms after leaving a ledge. | **Invisible UX Forgiveness**: 160ms hover grace on menus, expanded invisible hit-slop, and 4s optimistic undo windows. |
| **Hold-to-Commit (`M21`)** | Charging a heavy attack with rising pitch and tremor. | **Modal-Free Destructive Actions**: holding "Revoke" fills a tension gauge with rising frequency and smooth decay on early release. |
| **Pitch Escalation (`M20`)** | Collecting coins in sequence raises the musical note each time. | **Combo Checklists & Kanban Drops**: consecutive completions ascend `+2 semitones` (`440 * 2^(n/12)`) via Web Audio API. |
| **Damped Recoil (`M11`)** | Attacker steps back; target shakes on hit. | **Harmonic Error Shake (`±6px → 0px`)** on invalid inputs paired with a 140Hz→52Hz sub-bass thud. |

---

## The 3 Calibration Dials (Frequency vs. Intensity Guardrail)

A high-frequency B2B SaaS table must never animate like a slot machine. `game-feel-ui` enforces restraint through three orthogonal dials:

- **`--juice` (`1–10`)**: Visual kinematics (`--gf-press-scale`, `--gf-overshoot-scale`, `--gf-spring-stiffness`, `--gf-hitstop-ms`).
- **`--forgiveness` (`1–10`)**: Invisible ergonomics (`--gf-coyote-grace-ms`, `--gf-hit-slop-px`, `--gf-undo-window-ms`). Recommended at **`7–9`** for all productivity apps.
- **`--audio` (`0–10`)**: Procedural Web Audio API synthesizer gain (`--gf-audio-max-gain`) and haptic pulse intensity.

---

## Catalog & Stack Coverage

| Dataset | Items | Scope |
| :--- | :---: | :--- |
| [`data/mechanics.csv`](./data/mechanics.csv) | **39** | *Anticipation*, *Impact & Hitstop*, *Spring & Morph*, *Coyote Forgiveness*, *Spatial 3D*, *Progression & Audio* |
| [`data/components.csv`](./data/components.csv) | **23** | Component recipes across **L1 Subtle**, **L2 Balanced**, and **L3 Juicy** intensity tiers |
| [`data/audio-haptics.csv`](./data/audio-haptics.csv) | **11** | Zero-asset Web Audio API synthesizer recipes + `navigator.vibrate` patterns |
| [`data/physics-curves.csv`](./data/physics-curves.csv) | **7** | CSS `linear()`, `cubic-bezier`, and spring stiffness/damping/mass presets |
| [`data/app-profiles.csv`](./data/app-profiles.csv) | **8** | Vertical calibrations (*B2B SaaS, Fintech, EdTech, DevTools, E-Commerce, AI Workspace, Consumer, Creative*) |
| [`data/anti-patterns.csv`](./data/anti-patterns.csv) | **8** | 60fps compositor guardrails, audio fatigue prevention, and `prefers-reduced-motion` |
| [`data/stacks/*.csv`](./data/stacks/) | **11** | `react`, `nextjs`, `framer-motion`, `html-tailwind`, `css-waapi`, `gsap`, `shadcn`, `vue`, `svelte`, `react-native`, `flutter` |

---

## Validation & Tests

Zero external Python dependencies required (Python 3.8+ standard library):

```bash
python scripts/validate_data.py
python scripts/tests/test_game_feel.py
```

---

## License

MIT © [Eduardo Fiuza](https://github.com/e-fiuza)
