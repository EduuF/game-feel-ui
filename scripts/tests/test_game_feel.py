#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated test suite for game-feel-ui skill (core search, blueprint, audit, data contracts).
Run with: python scripts/tests/test_game_feel.py
"""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from core import AVAILABLE_STACKS, CSV_CONFIG, detect_domain, search, search_stack, _load_csv, DATA_DIR
from blueprint import generate_blueprint
from audit import audit_codebase
from validate_data import validate_all
from reasoning_contract import RULE_ACTIONS, evaluate_context_rules


class TestGameFeelSkill(unittest.TestCase):

    def test_data_contracts_valid(self):
        problems = validate_all()
        self.assertEqual(problems, [], f"Data contract errors: {problems}")

    def test_reasoning_contract_references(self):
        mech_ids = {r["Mechanic ID"] for r in _load_csv(DATA_DIR / "mechanics.csv")}
        comp_ids = {r["Component ID"] for r in _load_csv(DATA_DIR / "components.csv")}
        audio_ids = {r["Sound ID"] for r in _load_csv(DATA_DIR / "audio-haptics.csv")}
        for cond, act in RULE_ACTIONS.items():
            for m in act["mechanics"]:
                self.assertIn(m, mech_ids, f"Condition {cond} references unknown mechanic {m}")
            for c in act["components"]:
                self.assertIn(c, comp_ids, f"Condition {cond} references unknown component {c}")
            for a in act["audio"]:
                self.assertIn(a, audio_ids, f"Condition {cond} references unknown audio {a}")

        eval_res = evaluate_context_rules("kanban drag and drop with delete button and otp input")
        self.assertIn("if_kanban_drag", eval_res["activated_conditions"])
        self.assertIn("if_destructive", eval_res["activated_conditions"])
        self.assertIn("if_forms_validation", eval_res["activated_conditions"])

    def test_domain_search(self):
        for domain in CSV_CONFIG:
            res = search("button press spring click", domain=domain, max_results=2)
            self.assertNotIn("error", res)

    def test_mechanic_queries(self):
        hitstop = search("hitstop freeze frame", domain="mechanics")
        self.assertGreater(hitstop["count"], 0)
        self.assertEqual(hitstop["results"][0]["Mechanic ID"], "hitstop-micro-pause")

        coyote = search("coyote time hover dropdown", domain="mechanics")
        self.assertGreater(coyote["count"], 0)
        self.assertEqual(coyote["results"][0]["Mechanic ID"], "coyote-time-hover-grace")

    def test_auto_domain_detection(self):
        dom, _ = detect_domain("web audio synth pitch semitone oscillator")
        self.assertEqual(dom, "audio")
        dom2, _ = detect_domain("cubic-bezier spring config stiffness damping")
        self.assertEqual(dom2, "physics")
        dom3, _ = detect_domain("kanban card modal checkbox button")
        self.assertEqual(dom3, "components")

    def test_stack_search(self):
        for stack in AVAILABLE_STACKS:
            res = search_stack(stack, stack)
            self.assertNotIn("error", res)
            self.assertGreater(res["count"], 0, f"Stack {stack} returned 0 results")

    def test_blueprint_and_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            res = generate_blueprint(
                "SaaS productivity issue tracker kanban",
                project_name="Linear Clone",
                output_format="markdown",
                persist=True,
                component="kanban-card",
                output_dir=tmpdir,
                juice=5,
                forgiveness=7,
                audio=4,
            )
            self.assertIn("Game Feel UI Blueprint", res["text"])
            self.assertEqual(res["persistence"]["status"], "success")
            self.assertEqual(len(res["persistence"]["created_files"]), 2)

            # Second run without --force should skip overwriting MASTER.md
            res_skip = generate_blueprint(
                "SaaS productivity",
                project_name="Linear Clone",
                persist=True,
                output_dir=tmpdir,
            )
            self.assertEqual(res_skip["persistence"]["status"], "skipped_exists")

    def test_codebase_auditor(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "package.json").write_text(
                '{"dependencies": {"react": "^19.0.0", "tailwindcss": "^4.0.0"}}',
                encoding="utf-8",
            )
            (tmp_path / "App.tsx").write_text(
                """
                export function App({ totalCount }) {
                  return (
                    <div onMouseLeave={() => setOpen(false)} onMouseMove={(e) => setPos(e.clientX)}>
                      <button className="transition-all bg-blue-500">Save</button>
                      <button onClick={() => deleteWorkspace()}>Delete</button>
                      <span>{totalCount}</span>
                    </div>
                  );
                }
                """,
                encoding="utf-8",
            )
            report = audit_codebase(tmpdir)
            self.assertIn("react", report["stack_info"]["detected_stacks"])
            self.assertGreater(len(report["opportunities"]), 0)
            self.assertGreater(len(report["anti_patterns"]), 0)


if __name__ == "__main__":
    unittest.main()
