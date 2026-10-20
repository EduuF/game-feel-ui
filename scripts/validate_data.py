#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Integrity Validator for game-feel-ui skill.
Verifies:
  1. All configured domain and stack CSV files exist and parse cleanly.
  2. All search_cols and output_cols exist in each CSV header.
  3. Primary key ('No' and ID column) uniqueness.
  4. Cross-references:
     - Every 'Recommended Mechanics' ID in app-profiles.csv resolves to a valid Mechanic ID in mechanics.csv.
     - Every 'Mechanic Ref' in stacks/*.csv resolves to a valid Mechanic ID in mechanics.csv.
     - Every Mechanic row defines a non-empty 'Reduced Motion Fallback'.

Exits 0 on success, 1 on any contract violation.
"""

import csv
import sys
from pathlib import Path
from core import CSV_CONFIG, DATA_DIR, STACK_COLS, STACK_CONFIG


def _read_csv(filepath: Path):
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def validate_all() -> list:
    problems = []
    domain_rows = {}

    for domain, cfg in CSV_CONFIG.items():
        fpath = DATA_DIR / cfg["file"]
        if not fpath.exists():
            problems.append(f"[domain:{domain}] missing file {fpath}")
            continue
        headers, rows = _read_csv(fpath)
        domain_rows[domain] = rows
        if not rows:
            problems.append(f"[domain:{domain}] {fpath.name} has 0 data rows")
        hset = set(headers)
        for col in set(cfg["search_cols"]) | set(cfg["output_cols"]):
            if col not in hset:
                problems.append(f"[domain:{domain}] missing column '{col}' in {fpath.name}")

        seen_no = set()
        for i, r in enumerate(rows, 2):
            no_val = r.get("No", "")
            if no_val in seen_no:
                problems.append(f"[domain:{domain}] duplicate No '{no_val}' at line {i}")
            seen_no.add(no_val)

    # Check primary ID uniqueness across all domains
    id_columns = {
        "mechanics": "Mechanic ID",
        "components": "Component ID",
        "audio": "Sound ID",
        "physics": "Curve ID",
        "profiles": "Profile ID",
        "anti-patterns": "Anti-Pattern ID",
    }
    for dom, id_col in id_columns.items():
        seen_ids = set()
        for r in domain_rows.get(dom, []):
            val = r.get(id_col, "").strip()
            if not val:
                problems.append(f"[{dom}] row with empty {id_col}")
            elif val in seen_ids:
                problems.append(f"[{dom}] duplicate {id_col} '{val}'")
            seen_ids.add(val)

    # Check Mechanic IDs and Reduced Motion Fallbacks
    mechanic_ids = {r.get("Mechanic ID", "").strip() for r in domain_rows.get("mechanics", [])}
    for r in domain_rows.get("mechanics", []):
        mid = r.get("Mechanic ID", "").strip()
        if not r.get("Reduced Motion Fallback", "").strip():
            problems.append(f"[mechanics:{mid}] missing Reduced Motion Fallback")

    # Check Profile cross-references to Mechanic IDs
    for r in domain_rows.get("profiles", []):
        pid = r.get("Profile ID", "")
        rec = r.get("Recommended Mechanics", "")
        for mid in [m.strip() for m in rec.split("+") if m.strip()]:
            if mid not in mechanic_ids:
                problems.append(f"[profiles:{pid}] unresolved Mechanic ID '{mid}' in Recommended Mechanics")

    # Check Stack files and cross-references
    for stack, cfg in STACK_CONFIG.items():
        fpath = DATA_DIR / cfg["file"]
        if not fpath.exists():
            problems.append(f"[stack:{stack}] missing file {fpath}")
            continue
        headers, rows = _read_csv(fpath)
        if not rows:
            problems.append(f"[stack:{stack}] {fpath.name} has 0 rows")
        hset = set(headers)
        for col in set(STACK_COLS["search_cols"]) | set(STACK_COLS["output_cols"]):
            if col not in hset:
                problems.append(f"[stack:{stack}] missing column '{col}' in {fpath.name}")
        for r in rows:
            mref = r.get("Mechanic Ref", "").strip()
            if mref and mref not in mechanic_ids:
                problems.append(f"[stack:{stack}] unresolved Mechanic Ref '{mref}'")

    return problems


if __name__ == "__main__":
    issues = validate_all()
    if issues:
        for item in issues:
            print(f"ERROR: {item}", file=sys.stderr)
        sys.exit(1)
    print("OK: All game-feel-ui datasets and cross-references passed validation.")
    sys.exit(0)
