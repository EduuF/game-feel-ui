# Invisible Game Feel: Coyote Time, Input Buffering & Forgiveness Mechanics

The best Game Feel tricks are the ones the player **never consciously notices**, because their sole purpose is to make the human feel superhumanly accurate and the interface feel telepathically responsive.

In game development, if a player presses "Jump" 80ms *after* walking off a ledge (**Coyote Time**) or 80ms *before* landing on the ground (**Input Buffering**), the game still executes the jump. Without these two tricks, platformers feel frustrating and "unresponsive."

Here is how to implement all four pillars of **Invisible Forgiveness** in Web and Mobile UI.

---

## 1. Coyote Time in UI (Hover Grace & Deferred Destructive Commits)

### A. Menu & Tooltip Hover Grace (150ms)
When a user moves their cursor from a dropdown trigger or hover-card trigger toward the floating content, their cursor often crosses a 4px gap or briefly exits the boundary. Closing the menu in `0ms` on `mouseleave` is the UI equivalent of falling into a pit because you missed the ledge by 1 pixel.

```ts
// React Hook: useCoyoteHover(graceMs = 150)
import { useState, useRef, useCallback, useEffect } from 'react';

export function useCoyoteHover(graceMs = 150) {
  const [isOpen, setIsOpen] = useState(false);
  const timerRef = useRef<number | null>(null);

  const clearTimer = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const onPointerEnter = useCallback(() => {
    clearTimer();
    setIsOpen(true);
  }, [clearTimer]);

  const onPointerLeave = useCallback(() => {
    clearTimer();
    timerRef.current = window.setTimeout(() => {
      setIsOpen(false);
    }, graceMs);
  }, [clearTimer, graceMs]);

  useEffect(() => clearTimer, [clearTimer]);

  return { isOpen, setIsOpen, onPointerEnter, onPointerLeave };
}
```

### B. Toast Pause-on-Hover Coyote Time
Never auto-dismiss a toast notification while the user's pointer is inside the toast region or while the browser tab is hidden (`document.hidden`). Pause the countdown on `pointerenter`/`focusin` and resume on `pointerleave`.

### C. Deferred Commit Undo Window (4.5 Seconds)
Instead of interrupting flow with an *"Are you sure you want to delete this item?"* modal on routine actions:
1. Optimistically collapse and remove the item in `0ms` using a smooth 200ms height/opacity transition.
2. Start a `4500ms` timer before firing the irreversible `DELETE` or committing the soft-delete.
3. Show a compact toast with an **Undo** button (`<kbd>Z</kbd>`). If clicked, cancel the timer and spring the item back into its original slot.

---

## 2. Input Buffering (Never Drop a Fast User's Intent)

### A. Immediate Focus & Typeahead Buffering on Overlays
When a user presses `Cmd+K` to open a Command Palette or clicks "Search", the modal takes ~200ms to animate open. Power users start typing their query within **40ms** of pressing `Cmd+K`.
- **Anti-Pattern:** Focusing the `<input>` inside `onAnimationEnd` (drops the first 2–3 characters typed!).
- **Game-Feel Pattern:** Mount and `.focus()` the input synchronously at **Frame 0** while the container scales from `0.96 -> 1.0`.

### B. Non-Blocking Exit (`pointer-events: none` on Frame 0)
When a modal, backdrop scrim, or dropdown transitions to its `closed` state (even for 130ms), immediately apply `pointer-events: none` on the closing element and its backdrop so the user's very next click passes straight through to the underlying button they are aiming for.

```css
[data-state="closed"] {
  pointer-events: none !important;
  animation: fadeScaleOut 130ms cubic-bezier(0.4, 0, 1, 1) forwards;
}
```

---

## 3. Corner Correction & Aim Assist (Invisible Hitbox Expansion)

In action games, projectiles and ledges have slightly generous hitboxes for the player. In UI, small `16x16px` or `20x20px` icon buttons (Close `X`, Copy, More `...`, Checkbox, Slider thumb) cause constant near-miss clicks.

Expand the interactive hit area invisibly using `::after` without changing visual layout or spacing:

```css
.forgiving-hit-target {
  position: relative;
}
.forgiving-hit-target::after {
  content: "";
  position: absolute;
  inset: -8px; /* Adds 16px to width and height invisibly */
}
```

### Drag Distance Threshold (Preventing Accidental Drags)
When a card is both clickable (to open details) and draggable (to reorder in Kanban), a nervous click often moves the mouse by 2–3px between `pointerdown` and `pointerup`. Always enforce a **5px Euclidean distance threshold** (`Math.hypot(dx, dy) >= 5`) before transitioning from a click into a drag state.

---

## 4. Client-Side Prediction & Rollback Choreography (Optimistic UI)

Multiplayer games hide 80ms of network ping by moving your character on Frame 0 and reconciling with the server later. Web applications should treat REST/GraphQL/Server Actions the exact same way:

1. **Frame 0 (Prediction):** On click, immediately flip the toggle/like/checkbox/kanban slot and play the tactile spring animation.
2. **In-Flight:** Do not block the UI with a spinner for routine mutations.
3. **Server Rejects (Rollback Choreography):** If the request fails, revert the state, trigger a 300ms **Damped Trauma Shake** (`±6px -> 0px`) on the control, play the muted double-thud error sound, and announce the error via an `aria-live="assertive"` toast.
