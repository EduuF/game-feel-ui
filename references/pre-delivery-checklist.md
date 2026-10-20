# Game Feel UI — Canonical Audit & Pre-Delivery Checklist

Run through this checklist before delivering any Game Feel / Micro-interaction implementation or when auditing an existing codebase.

---

## 1. Frequency × Intensity Budget (Anti-Fatigue Check)
- [ ] **High-Frequency Subliminal Controls** (nav links, standard buttons, tabs, inputs, filters) complete within **100ms–180ms**, scale within `0.965–1.02`, and have **zero** hitstop delay or particle bursts.
- [ ] **Medium-Frequency Kinetic Controls** (toggles, checkboxes, Kanban cards, copy buttons, modals) use physics/spring curves (`cubic-bezier(0.22, 1, 0.36, 1)` or `cubic-bezier(0.34, 1.56, 0.64, 1)`) and complete within **180ms–320ms**.
- [ ] **Low-Frequency Hero Moments** (deploy, publish, milestone complete, hold-to-delete) are limited to **1–3 focal moments** across the application where Hitstop (70–100ms), Specular Sheen, or Localized Particle Bursts (≤14 sparks) create memorable delight.

## 2. Tactile Physics & Temporal Choreography
- [ ] **Tactile Press Compression (`:active`):** Every interactive button/card has an immediate `50–75ms` press-in response (`active:scale-[0.97] active:translate-y-[1px]`) and a slightly longer (`150–180ms`) spring release.
- [ ] **Asymmetric Enter vs. Exit:** Overlays (modals, dropdowns, drawers, toasts) exit **35–45% faster** (`110–145ms` ease-in) than they enter (`200–260ms` ease-out/spring).
- [ ] **Origin-Aware Scaling:** Dropdowns, popovers, and context menus scale from their trigger corner (`transform-origin`), never from the dead center of the screen unless they are centered dialogs.
- [ ] **Text Distortion Guard:** Squash & stretch or `layoutId` morphs are applied strictly to background pills, thumbs, or icons—never warping text glyphs.
- [ ] **Numeric Stability:** All animated counters, prices, timers, and badge counts enforce `font-variant-numeric: tabular-nums` (`tabular-nums`).

## 3. Invisible Forgiveness (Coyote Time & Input Buffering)
- [ ] **Coyote Time Hover Grace:** Hover-triggered menus, tooltips, and popovers include a `150ms` grace period on `pointerleave` so diagonal cursor travel never snaps them shut prematurely.
- [ ] **Toast Hover Pause:** Toast auto-dismiss timers pause on `pointerenter` and `focusin`.
- [ ] **Non-Blocking Exits:** Closing modals, backdrops, and popovers immediately apply `pointer-events: none` at Frame 0 of exit so rapid clicks pass through to underlying controls.
- [ ] **Immediate Input Focus:** Opening a Command Palette (`Cmd+K`) or search dialog focuses the `<input>` at Frame 0, never waiting for `onAnimationEnd`.
- [ ] **Invisible Hitbox Expansion:** Compact icon buttons (`<32px` visual size) include an invisible `::after { inset: -8px }` hit zone to reach `≥44x44px` touch/click comfort.
- [ ] **Optimistic State + Rollback:** Routine state toggles (like, bookmark, checkbox, switch) update in `0ms` optimistically and choreograph a damped `traumaShake` rollback only if the server request fails.

## 4. Compositor Performance & Accessibility
- [ ] **60/120fps Compositor Budget:** Animations mutate only `transform` (`translate3d`, `scale3d`, `rotate`) and `opacity` (or `grid-template-rows` / FLIP). Zero animations on `width`, `height`, `top`, `left`, or `margin`.
- [ ] **No React State Thrashing on PointerMove:** Magnetic buttons, radial spotlights, and 3D tilt cards update CSS variables or `useMotionValue` via `ref`, never calling `useState` setter on `pointermove`.
- [ ] **`prefers-reduced-motion` Compliance:** Spatial translations, 3D tilts, trauma shakes, hitstop pauses, and particle bursts are disabled or reduced to crisp `<=100ms` opacity/color transitions when `@media (prefers-reduced-motion: reduce)` matches.
- [ ] **DOM & Timer Cleanup:** Dynamically spawned ripple/particle nodes remove themselves in `.onfinish`, and all `setTimeout` / `requestAnimationFrame` / `AudioContext` resources clean up on unmount.
