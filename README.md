# 🎮 `game-feel-ui` — Claude Code Skill

**Game Feel, Juiciness, Invisible Forgiveness & Sensory UI Intelligence for Web, Mobile & Desktop Applications.**

Inspired by game development masters (Steve Swink's *Game Feel*, Vlambeer's *Art of Screenshake*, Martin Jonasson & Petri Purho's *Juice it or lose it*, and *Celeste*'s Coyote Time & Input Buffering), this skill equips Claude Code to **audit existing applications** and **implement subtle, high-craft kinesthetic micro-interactions** without causing "slot-machine fatigue."

---

## 📂 Directory Structure

```text
game-feel-ui/
├── SKILL.md                              # Main Claude Code skill definition & workflow
├── README.md                             # Installation & CLI usage documentation
├── data/
│   ├── mechanics.csv                     # 29 Game Dev techniques translated to DOM/UI specs & snippets
│   ├── components.csv                    # 15 UI component 5-stage choreography recipes
│   ├── audio-haptics.csv                 # 8 zero-dependency Web Audio API procedural synth & haptic recipes
│   ├── physics-curves.csv                # 7 exact spring/bezier curves (CSS linear(), Framer Motion, GSAP)
│   ├── app-profiles.csv                  # 8 product archetypes with Juice Budgets & reasoning
│   ├── anti-patterns.csv                 # 8 critical Game Feel UI anti-patterns & fixes
│   ├── catalog-summary.json              # Dataset integrity & counts manifest
│   └── stacks/                           # 11 stack-specific implementation guides
│       ├── react.csv
│       ├── nextjs.csv
│       ├── framer-motion.csv
│       ├── html-tailwind.csv
│       ├── css-waapi.csv
│       ├── gsap.csv
│       ├── shadcn.csv
│       ├── vue.csv
│       ├── svelte.csv
│       ├── react-native.csv
│       └── flutter.csv
├── references/
│   ├── game-feel-principles.md           # Swink, Vlambeer, Disney 12 Principles & Frequency Matrix
│   ├── coyote-time-and-forgiveness.md    # Coyote Time, Input Buffering, Aim Assist & Optimistic UI
│   ├── procedural-web-audio.md           # Drop-in TypeScript Web Audio & Haptics Engine
│   └── pre-delivery-checklist.md         # Canonical 20-point quality & accessibility checklist
└── scripts/
    ├── search.py                         # Unified CLI (Search, Blueprint Generator, Codebase Auditor)
    ├── core.py                           # Pure-stdlib BM25 search engine with auto-domain routing
    ├── blueprint.py                      # Game Feel Blueprint generator with Dials & Persistence
    ├── audit.py                          # Static codebase Game-Feel scanner & scorer (0-100)
    ├── validate_data.py                  # Schema & cross-reference integrity validator
    └── tests/
        └── test_game_feel.py             # Automated unit test suite
```

---

## 🚀 Installation in Claude Code

Copy or symlink this folder into your global Claude skills directory or your repository's `.claude/skills/` directory:

```powershell
# Global installation (available in all projects)
git clone https://github.com/EduuF/game-feel-ui.git ~/.claude/skills/game-feel-ui

# Or via npx skills CLI
npx skills add EduuF/game-feel-ui
```

---

## 🛠️ CLI Quick Start

### 1. Audit an Existing Codebase for Game Feel Opportunities
```bash
python scripts/search.py --audit "/path/to/your/webapp/src"
```

### 2. Generate a Complete Game Feel Blueprint (with Sensory Dials)
```bash
python scripts/search.py "saas kanban productivity" --blueprint -p "My WebApp" --juice 5 --forgiveness 7 --audio 4
```

### 3. Search Specific Domains & Stacks
```bash
python scripts/search.py "hitstop freeze frame" --domain mechanics
python scripts/search.py "coyote time dropdown" --domain mechanics
python scripts/search.py "copy to clipboard" --domain components
python scripts/search.py "combo pitch semitone" --domain audio
python scripts/search.py "whileTap layoutId" --stack framer-motion
```

### 4. Validate Datasets & Run Tests
```bash
python scripts/validate_data.py
python scripts/tests/test_game_feel.py
```
