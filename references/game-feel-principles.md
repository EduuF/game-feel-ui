# Game Feel, Juiciness & Sensory UI — Core Principles

Load this reference when designing interaction choreography, choosing intensity tiers, or explaining the theoretical bridge between Game Engines and DOM/Mobile Application UI.

---

## 1. The Theoretical Bridge: Swink, Vlambeer & Disney

1. **Game Feel (Steve Swink):** The tactile, kinesthetic sensation of manipulating virtual objects in real time. It is built on three pillars:
   - **Real-Time Control:** Instantaneous (<16ms) response to pointer/keyboard input with continuous velocity and momentum tracking.
   - **Simulated Space:** Virtual UI surfaces behave as if they possess mass, elasticity, friction, and spatial continuity (cards lift and cast shadows when dragged; boundaries push back with viscous rubber-banding).
   - **Polish (Juice):** Cascading multi-sensory feedback (visual, temporal, spatial, auditory, haptic) that affirms the user's action.

2. **Juiciness ("Juice it or lose it" — Jonasson & Purho):**
   - A "dry" interface gives a 1:1 binary response (click button → text changes).
   - A "juicy" interface gives a **cascading, multi-layered response** within the first 50–250ms:
     1. **Anticipation (0–60ms):** On `pointerdown`, the button compresses (`scale(0.965) translateY(1px)`), storing virtual potential energy like a coiled spring.
     2. **Impact / Hitstop (0–90ms on release):** On `pointerup`, a radial pulse originates at `(x, y)`, an optional 75ms hitstop pause adds weight on Hero actions, and a 10ms procedural click sounds.
     3. **Follow-Through & Overlapping Action (90–300ms):** The button springs back (`cubic-bezier(0.34, 1.56, 0.64, 1)`), the icon morphs elastically into a checkmark, and adjacent elements nudge or update their counters via an odometer roll.

---

## 2. The Golden Rule of Application UI: The Frequency × Intensity Matrix

Game engines aim to maximize sensory stimulation. Software applications aim to **maximize flow state and perceived responsiveness** without causing **"Slot-Machine Fatigue"**.

Every interactive element in an application MUST be classified into one of three tiers before applying Game Feel:

| Tier | Examples | Max Duration | Scale Delta | Allowed Mechanics | Forbidden Mechanics |
|------|----------|--------------|-------------|-------------------|---------------------|
| **Tier 1: High-Frequency Subliminal** *(50+ times/session)* | Nav links, standard buttons, tabs, inputs, dropdowns, table filters, Cmd+K | **100ms – 180ms** | `0.965` – `1.02` | Tactile press compression, Coyote Time hover grace, Input Buffering, Invisible Hitbox expansion, FLIP active pill glide, Asymmetric fast exit | Hitstop delays, Particle bursts, Screen/card shake, Chime melodies, Bouncy >5% overshoot |
| **Tier 2: Medium-Frequency Kinetic** *(5–30 times/session)* | Checkboxes, toggles, Kanban drag-and-drop, copy-to-clipboard, likes, modals, validation errors, sliders | **180ms – 320ms** | `0.90` – `1.12` | Spring overshoot (`back.out`), Squash & stretch on thumbs/badges, Neighbor knockback (FLIP), Damped trauma shake on error, Odometer number roll, Detent ticks, Optimistic commit | Full-screen confetti, Blocking modal dialogs for routine deletes, Uncapped stagger delays (>150ms total) |
| **Tier 3: Low-Frequency Hero Moments** *(1–3 times/session)* | Deploy to production, Publish workflow, Complete onboarding, Inbox Zero, Checkout payment, Delete workspace | **300ms – 650ms** *(+ 800ms hold if destructive)* | `0.92` – `1.20` | **Full Arsenal:** Hold-to-confirm charge-up, 80ms Hitstop micro-pause, Localized particle micro-burst (6–12 sparks), Specular sheen sweep, Receding background depth scale, Harmonic triad chime | Uninterruptible 3-second cutscenes that block the user from continuing work |

---

## 3. Translating Disney's 12 Principles to DOM Components

| Disney Principle | Game Dev Usage | Web / App UI Implementation |
|------------------|----------------|-----------------------------|
| **1. Squash & Stretch** | Ball flattens on floor impact and elongates in mid-air | Toggle switch thumb widens (`width: 22px` or `scaleX(1.15)`) while sliding; checkbox pops (`1.12, 0.88` -> `1, 1`). *Never squash text nodes.* |
| **2. Anticipation** | Character crouches before jumping or pulls sword back | `:active` compression (`scale(0.965)`) on `pointerdown`; dropzone icon floats up `-5px` when a file is dragged into the window. |
| **3. Staging** | Spotlight dims the stage around the main actor | Receding background shell (`scale(0.975)`) + scrim dimming when a primary modal or command palette opens; perimeter border beam on active AI prompt. |
| **4. Follow-Through & Overlapping Action** | Cape and hair keep moving after the hero stops running | Modal container lands at 200ms; internal icon, heading, and CTA stagger-settle at `+25ms`, `+50ms`, `+75ms`. |
| **5. Slow In & Slow Out (Asymmetric Easing)** | Cars accelerate slowly and brake smoothly | **Asymmetric Enter/Exit:** Elements enter with deceleration (`cubic-bezier(0.22, 1, 0.36, 1)`, 240ms) and exit with crisp acceleration (`cubic-bezier(0.4, 0, 1, 1)`, 130ms). |
| **6. Arcs** | Thrown projectiles follow parabolic curves | Dragged Kanban cards tilt slightly (`rotateZ(±3deg)`) proportional to horizontal velocity; floating badges arc into counters. |
| **7. Secondary Action** | Facial expression changes while swinging a hammer | Clicking "Add to Cart" compresses the button (primary) while the navbar cart badge pops and rolls its digit upward (secondary). |
| **8. Timing (Hitstop)** | 4-frame freeze when a heavy attack connects | 80ms freeze at `scale(0.94)` before releasing the "Published!" expansion and particle sparks. |
| **9. Exaggeration** | Oversized hit sparks and recoil | Brief `scale(1.25)` peak on a Heart/Bookmark icon before settling to `scale(1.0)`. |
| **10. Solid Drawing (Mass & Depth)** | Consistent 3D volume and lighting | Elevated diffused shadow + `scale(1.04)` on dragged cards; top-edge `1px` specular inset highlight (` inset 0 1px 0 rgba(255,255,255,0.15)`) on buttons. |
| **11. Appeal** | Tactile, memorable character feel | Zero-jitter `tabular-nums` counters, responsive `<kbd>` keycaps that depress when typed, and warm procedural clicks. |
