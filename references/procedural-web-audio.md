# Procedural Web Audio & Haptics Engine (Zero External Assets)

Load this reference when adding subtle acoustic feedback or mobile haptics to a web application.

Why procedural synthesis via the **Web Audio API** instead of `.mp3` / `.wav` files?
1. **Zero network requests, 0 KB bundle size, 0ms decode latency.**
2. **Real-time parametric modulation:** You can dynamically shift pitch by `+1 semitone` per consecutive combo action (`2^(step/12)`) or vary filter cutoff by drag velocity—impossible with static audio files without pitch-stretching artifacts.
3. **Subliminal acoustic design:** Short (6–25ms), low-gain (`0.03`–`0.06`) sine/triangle impulses feel like physical hardware switches rather than "sound effects."

---

## Drop-In TypeScript/JavaScript Module (`gameFeelAudio.ts`)

```ts
/**
 * Zero-dependency Procedural UI Sound & Haptics Engine.
 * Respects user mute preferences and lazy-initializes a singleton AudioContext on user gesture.
 */
class GameFeelSensoryEngine {
  private ctx: AudioContext | null = null;
  private enabled: boolean = true;
  private comboStep: number = 0;
  private lastComboTime: number = 0;

  private getContext(): AudioContext | null {
    if (!this.enabled || typeof window === 'undefined') return null;
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (!AudioCtx) return null;
      this.ctx = new AudioCtx();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume().catch(() => {});
    }
    return this.ctx;
  }

  public setEnabled(enabled: boolean) {
    this.enabled = enabled;
  }

  public haptic(pattern: number | number[] = 5) {
    if (!this.enabled || typeof navigator === 'undefined') return;
    navigator.vibrate?.(pattern);
  }

  /**
   * 1. Crisp Tactile Switch Click (10ms) — High-frequency buttons, tabs, keycaps
   */
  public click() {
    this.haptic(4);
    const ctx = this.getContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(1200, t);
    osc.frequency.exponentialRampToValueAtTime(180, t + 0.009);
    gain.gain.setValueAtTime(0.035, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.01);
    osc.connect(gain).connect(ctx.destination);
    osc.start(t);
    osc.stop(t + 0.011);
  }

  /**
   * 2. State Toggle Pop (28ms) — Checkboxes, switches, likes
   */
  public pop(active: boolean = true) {
    this.haptic(6);
    const ctx = this.getContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(active ? 340 : 580, t);
    osc.frequency.exponentialRampToValueAtTime(active ? 680 : 300, t + 0.025);
    gain.gain.setValueAtTime(0.05, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.028);
    osc.connect(gain).connect(ctx.destination);
    osc.start(t);
    osc.stop(t + 0.03);
  }

  /**
   * 3. Pitch-Escalating Combo Tick (30ms) — Sequential task checks, multi-select, streaks
   * Rises by +1 semitone per consecutive hit within 2000ms (capped at +12 semitones).
   */
  public combo() {
    this.haptic(5);
    const ctx = this.getContext();
    if (!ctx) return;
    const now = performance.now();
    this.comboStep = now - this.lastComboTime < 2000 ? Math.min(this.comboStep + 1, 12) : 0;
    this.lastComboTime = now;

    const freq = 320 * Math.pow(2, this.comboStep / 12);
    const t = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, t);
    osc.frequency.exponentialRampToValueAtTime(freq * 1.35, t + 0.025);
    gain.gain.setValueAtTime(0.055, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.03);
    osc.connect(gain).connect(ctx.destination);
    osc.start(t);
    osc.stop(t + 0.032);
  }

  /**
   * 4. Muted Double-Thud Error Reject (140ms) — Form validation failure, shake rollback
   */
  public error() {
    this.haptic([25, 40, 25]);
    const ctx = this.getContext();
    if (!ctx) return;
    [0, 0.07].forEach((offset) => {
      const t = ctx.currentTime + offset;
      const osc = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(150, t);
      osc.frequency.linearRampToValueAtTime(125, t + 0.05);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(420, t);
      gain.gain.setValueAtTime(0.05, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.055);
      osc.connect(filter).connect(gain).connect(ctx.destination);
      osc.start(t);
      osc.stop(t + 0.06);
    });
  }

  /**
   * 5. Hero Triad Chime (400ms) — Milestone unlocked, deployment live, onboarding 100%
   */
  public heroChime() {
    this.haptic([10, 50, 20]);
    const ctx = this.getContext();
    if (!ctx) return;
    [523.25, 659.25, 783.99].forEach((freq, i) => {
      const t = ctx.currentTime + i * 0.065;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, t);
      gain.gain.setValueAtTime(0.05, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.38);
      osc.connect(gain).connect(ctx.destination);
      osc.start(t);
      osc.stop(t + 0.4);
    });
  }
}

export const sensory = new GameFeelSensoryEngine();
```
