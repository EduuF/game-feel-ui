---
name: game-feel-ui
description: "Game Feel, Juiciness & Sensory UI intelligence for web, mobile, and desktop applications. Use this skill when evaluating/auditing an existing application for subtle engagement opportunities, adding tactile micro-interactions, spring physics, hitstop tension, squash-and-stretch morphing, Coyote Time hover/undo forgiveness, input buffering, optimistic UI rollback choreography, procedural Web Audio SFX, or haptics. Searchable local database: 29 Game Dev-to-UI mechanics, 15 multi-layered component choreography recipes, 8 zero-asset procedural Web Audio synths, 7 spring/bezier physics curves, 8 product juice profiles, 8 anti-patterns, 11 stack guides, plus a static codebase auditor (--audit)."
---

# Game Feel UI — Tactile, Kinesthetic & Sensory Application Intelligence

Translates **Game Feel** (Steve Swink), **Juiciness** (Vlambeer / Jonasson & Purho), **Invisible Forgiveness** (Coyote Time, Input Buffering, Aim Assist), and **Disney's 12 Principles of Animation** into subtle, high-craft engagement for modern Web, Mobile, and Desktop applications.

---

## When to Apply

Activate this skill when the user wants to:
1. **Audit / Evaluate an existing codebase** to discover where subtle Game Dev engagement techniques can make the interface feel more alive, tactile, forgiving, and responsive.
2. **Design or upgrade UI components** (buttons, toggles, checkboxes, Kanban boards, modals, command palettes, forms, counters, AI streaming inputs) with multi-layered sensory feedback.
3. **Fix "dead", "laggy", or "frustrating" interactions** using Invisible Game Feel (Coyote Time menu grace periods, Input Buffering, Invisible Hitbox expansion, Optimistic UI with trauma-shake rollback).
4. **Add zero-dependency Procedural Web Audio SFX or Haptics** (tactile switch clicks, pitch-escalating combo ticks, harmonic completion chimes).

---

## The Golden Rule: The Frequency × Intensity Matrix

Never turn a productivity or SaaS application into an exhausting slot machine. Classify every interaction into one of three tiers before choosing mechanics:

| Priority Tier | Usage Frequency | Max Duration | Scale Delta | Allowed Mechanics | Forbidden Anti-Patterns |
|---------------|-----------------|--------------|-------------|-------------------|-------------------------|
| **1. High-Frequency Subliminal** | **50+ times/session** *(Nav, standard buttons, tabs, inputs, filters, Cmd+K)* | **100ms – 180ms** | `0.965` – `1.02` | Tactile press (`active:scale-[0.97]`), Coyote Time hover grace (`150ms`), Input Buffering (`0ms` focus), Invisible Hitbox (`::after -8px`), FLIP pill glide, Asymmetric fast exit (`130ms`) | Hitstop delays, Particle bursts, Screen/card shake, Chime melodies, Bouncy >5% overshoot |
| **2. Medium-Frequency Kinetic** | **5–30 times/session** *(Toggles, checkboxes, Kanban drag, copy button, modals, sliders, KPIs)* | **180ms – 320ms** | `0.90` – `1.12` | Spring overshoot (`cubic-bezier(0.34,1.56,0.64,1)`), Squash & stretch on thumbs/badges, Neighbor knockback (FLIP), Damped trauma shake on error, Odometer number roll (`tabular-nums`), Detent ticks, Optimistic commit | Full-screen confetti, Blocking modal dialogs for routine deletes, Uncapped stagger delays (>150ms total) |
| **3. Low-Frequency Hero Moments** | **1–3 times/session** *(Deploy, Publish, Onboarding 100%, Inbox Zero, Checkout, Delete Workspace)* | **300ms – 650ms** *(+ 800ms hold if destructive)* | `0.92` – `1.20` | **Full Arsenal:** Hold-to-confirm charge-up, 85ms Hitstop micro-pause, Localized particle micro-burst (6–12 sparks), Specular sheen sweep, Receding background depth scale, Harmonic triad chime | Uninterruptible 3-second cutscenes that block user input |

---

## Running the CLI Tool (`search.py`)

Resolve the script path relative to this skill's directory (e.g., `~/.claude/skills/game-feel-ui/scripts/search.py` or `.claude/skills/game-feel-ui/scripts/search.py` or the current skill folder):

```bash
python "<SKILL_DIR>/scripts/search.py" --help
```

Requires Python 3.x (pure standard library, zero external packages).

---

## Workflow

### Mode A: Auditing an Existing Application (`--audit`)

When the user asks to **evaluate their app**, **find opportunities for subtle game-feel engagement**, or **suggest improvements to an existing project**:

#### Step 1: Run the Static Codebase Auditor
```bash
python "<SKILL_DIR>/scripts/search.py" --audit "<path-to-user-project-or-src>"
```
This scans `.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`, `.css`, and `package.json`, outputting:
- **Detected Stack & Motion Libraries** (`react`, `nextjs`, `framer-motion`, `html-tailwind`, `shadcn`, `gsap`, `vue`, `svelte`, etc.)
- **Overall Juice Score (0–100)** broken down across *Tactile Physics*, *Forgiveness (Coyote/Buffer)*, *Sensory & Numeric Polish*, and *Compositor & A11y Safety*.
- **Detected Anti-Patterns (`file:line`)** (e.g., `zero-coyote-hover-trap` where `onMouseLeave={() => setOpen(false)}` snaps menus shut, `pointermove-state-thrash`, or `transition-all` layout thrashing).
- **Prioritized Game Feel Opportunities (`file:line`)** mapped to exact `Mechanic ID`s (`anticipation-press`, `charge-up-anticipation`, `icon-elastic-morph`, `squash-and-stretch-morph`, `drag-elevation-shadow`, `odometer-number-roll`, etc.).

#### Step 2: Inspect the Flagged Components & Generate a Blueprint
Read the key component files flagged by `--audit`, then generate a tailored **Game Feel Blueprint** for the application's product archetype:
```bash
python "<SKILL_DIR>/scripts/search.py" "<product_type> <keywords>" --blueprint -p "Project Name"
```

#### Step 3: Query Specific Mechanics, Components, and Stack Idioms
Query the exact mechanics and stack guidelines before writing code:
```bash
# Search specific mechanic spec + snippet
python "<SKILL_DIR>/scripts/search.py" "hitstop freeze frame" --domain mechanics

# Search multi-layered component choreography (Wind-up -> Impact -> Settle -> Forgiveness -> Audio)
python "<SKILL_DIR>/scripts/search.py" "kanban draggable card" --domain components

# Search stack-specific implementation rules
python "<SKILL_DIR>/scripts/search.py" "optimistic press" --stack react
python "<SKILL_DIR>/scripts/search.py" "whileTap layoutId" --stack framer-motion
```

---

### Mode B: Designing a New Feature or System-Wide Game Feel Blueprint (`--blueprint`)

Use `--blueprint` (or `-bp`) with three optional 1–10 sensory dials (`--juice`, `--forgiveness`, `--audio`):

```bash
python "<SKILL_DIR>/scripts/search.py" "saas issue tracker kanban" --blueprint --juice 5 --forgiveness 8 --audio 4 -p "TaskFlow"
```

| Sensory Dial | Low (1–3) | Mid (4–7) | High (8–10) |
|--------------|-----------|-----------|-------------|
| `--juice` | **Subliminal & Crisp:** 120ms max high-freq, `0.975` press scale, zero bounce | **Kinetic & Tactile:** 150ms high-freq, `0.965` press scale, subtle ~4% spring overshoot | **Expressive & Celebratory:** Gamified bounce, squash & stretch, hero bursts |
| `--forgiveness` | **Standard:** 100ms hover grace, +4px hitboxes | **Generous:** 150ms Coyote Time, +8px invisible hitboxes, 4.5s Undo toast | **Maximum Assist:** 180ms Coyote Time, +12px hitboxes, magnetic pull, 5s Undo |
| `--audio` | **Silent / Haptic Only:** Zero desktop audio; mobile `navigator.vibrate(4)` | **Subliminal Hardware Ticks:** Opt-in `<=0.04` gain 10ms switch clicks + combo ramp | **Full Procedural Suite:** Switch clicks, bubble pops, drop thuds, hero triad chimes |

#### Persisting the Blueprint (`--persist`)
To save the Game Feel Blueprint across sessions (Master + Component Overrides pattern):
```bash
python "<SKILL_DIR>/scripts/search.py" "saas workspace" --blueprint --persist -p "TaskFlow" --output-dir "<project-root>" --component "command-palette"
```
This creates:
- `game-feel/<project-slug>/MASTER.md` — Global CSS tokens (`--gf-press-scale`, `--gf-ease-spring`, `--gf-coyote-grace`), Frequency Budget, and core mechanics.
- `game-feel/<project-slug>/components/<component>.md` — Component-specific choreography override.

---

## Available Search Domains (`--domain`) & Stacks (`--stack`)

| Domain (`--domain`) | Dataset | What It Returns |
|---------------------|---------|-----------------|
| `mechanics` | `data/mechanics.csv` (29 rows) | Game Dev origin, UI equivalent, frequency tier, timing/physics spec, CSS/JS snippet, reduced-motion fallback |
| `components` | `data/components.csv` (15 rows) | 5-layer recipe per UI component: **Anticipation (Wind-up)**, **Impact**, **Follow-Through**, **Forgiveness**, **Audio/Haptic**, and **Code Recipe** |
| `audio` | `data/audio-haptics.csv` (8 rows) | Zero-asset Web Audio API procedural synth snippets (`AudioContext` oscillators/filters) + mobile haptic patterns |
| `physics` | `data/physics-curves.csv` (7 rows) | Exact `cubic-bezier()`, CSS `linear()` springs, Framer Motion spring configs, and GSAP eases |
| `profiles` | `data/app-profiles.csv` (8 rows) | Product-type Juice Budgets (SaaS, Fintech, E-commerce, AI Chat, EdTech, Analytics, Creative Tool, Marketing) |
| `anti-patterns` | `data/anti-patterns.csv` (8 rows) | Common Game-Feel UI mistakes (Slot-Machine Fatigue, Laggy Hitstop Misuse, Zero-Coyote Hover Trap, etc.) and fixes |

**Available Stacks (`--stack`):** `react`, `nextjs`, `framer-motion`, `html-tailwind`, `css-waapi`, `gsap`, `shadcn`, `vue`, `svelte`, `react-native`, `flutter`.

---

## On-Demand Deep Reference Guides

Load these files from `references/` when needed:
- `references/game-feel-principles.md` — Deep theory (Swink, Vlambeer, Disney's 12 Principles in the DOM, Frequency × Intensity Matrix).
- `references/coyote-time-and-forgiveness.md` — Drop-in patterns for `useCoyoteHover`, Safe Triangles, Input Buffering, Invisible Hitbox expansion, and Optimistic Rollback Choreography.
- `references/procedural-web-audio.md` — Complete copy-pasteable TypeScript/JS `GameFeelSensoryEngine` class (`click()`, `pop()`, `combo()`, `error()`, `heroChime()`).
- `references/pre-delivery-checklist.md` — Canonical 20-point verification checklist before delivering code.
