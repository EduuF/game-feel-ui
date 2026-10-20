# Contributing to `game-feel-ui`

Contributions of new Game Feel mechanics, UI component recipes, Web Audio synthesizer patterns, and framework stack implementations are welcome.

## Project Structure

- `SKILL.md` — Main agent entrypoint and orchestration rules.
- `data/mechanics.csv` — Core Game Dev mechanics translated to UI physics (`M01`–`M39+`).
- `data/components.csv` — Component-level recipes across L1 (Subtle), L2 (Balanced), and L3 (Juicy) tiers.
- `data/audio-haptics.csv` — Zero-asset Web Audio API synthesizer recipes and vibration patterns.
- `data/physics-curves.csv` — Spring and easing presets.
- `data/app-profiles.csv` — Default `--juice`, `--forgiveness`, and `--audio` dials per vertical.
- `data/anti-patterns.csv` — UX and 60fps performance guardrails.
- `data/stacks/*.csv` — Framework-specific code implementations.
- `scripts/` — Zero-dependency Python 3 BM25 search engine, static codebase auditor, and blueprint generator.

## Validation Workflow

Before submitting a Pull Request, run the schema validator and unit test suite (requires only Python 3.8+ standard library):

```bash
# 1. Validate CSV headers, cross-references, and catalog-summary.json
python scripts/validate_data.py

# 2. Run the unit test suite
python scripts/tests/test_game_feel.py
```

If you add rows to any CSV file, update the corresponding count in `data/catalog-summary.json`.
