#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Feel UI CLI — Unified Search, Blueprint Generator & Codebase Auditor.

Usage:
  1. Audit an existing application codebase for Game Feel opportunities:
     python search.py --audit "<path-to-project>"

  2. Generate a complete Game Feel Blueprint for an app/feature:
     python search.py "<query>" --blueprint [-p "Project Name"] [--juice 1-10] [--forgiveness 1-10] [--audio 1-10]
     python search.py "<query>" --blueprint --persist -p "Project Name" --output-dir "<project-root>" [--component "kanban-card"]

  3. Search specific Game Feel domains (mechanics, components, audio, physics, profiles, anti-patterns):
     python search.py "<query>" [--domain <domain>] [-n 3]

  4. Search stack-specific implementation patterns:
     python search.py "<query>" --stack <stack>
"""

import argparse
import io
import json
import sys
from core import AVAILABLE_STACKS, CSV_CONFIG, MAX_RESULTS, UNTRUNCATED_COLS, search, search_stack
from blueprint import generate_blueprint
from audit import audit_codebase, format_audit_report

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

TRUNCATE_AT = 360


def format_search_output(result: dict, full: bool = False) -> str:
    if "error" in result:
        return f"Error: {result['error']}"

    out = []
    if result.get("stack"):
        out.append("## 🎮 Game Feel UI — Stack Implementation Guidelines")
        out.append(f"**Stack:** `{result['stack']}` | **Query:** `{result['query']}`")
    else:
        out.append("## 🎮 Game Feel UI — Search Results")
        dom = result["domain"]
        if result.get("auto_detected"):
            dom += " (auto-detected"
            if result.get("runner_up_domain"):
                dom += f", runner-up: {result['runner_up_domain']}"
            dom += ")"
        out.append(f"**Domain:** `{dom}` | **Query:** `{result['query']}`")
    out.append(f"**Source:** `{result['file']}` | **Found:** {result['count']} results\n")

    if result["count"] == 0:
        out.append(
            "No exact database matches found. Retry with 2-4 core terms "
            "(e.g., 'hitstop', 'coyote time', 'button press', 'kanban drag', 'error shake')."
        )
        if result.get("suggestions"):
            out.append(f"**Closest indexed terms:** {', '.join(result['suggestions'])}")
        return "\n".join(out)

    for i, row in enumerate(result["results"], 1):
        out.append(f"### Result {i}")
        for k, v in row.items():
            v_str = str(v)
            if not full and k not in UNTRUNCATED_COLS and len(v_str) > TRUNCATE_AT:
                v_str = v_str[:TRUNCATE_AT] + "..."
            out.append(f"- **{k}:** {v_str}")
        out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Game Feel UI — Search, Blueprint & Codebase Audit CLI")
    parser.add_argument("query", nargs="?", default="", help="Search query or product description")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Domain to search")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help=f"Stack guide: {', '.join(AVAILABLE_STACKS)}")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results (1-20)")
    parser.add_argument("--full", action="store_true", help="Do not truncate long fields")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # Codebase Audit mode
    parser.add_argument("--audit", "-a", type=str, default=None, metavar="PATH",
                        help="Scan a frontend codebase directory or file for Game Feel opportunities and anti-patterns")

    # Blueprint mode
    parser.add_argument("--blueprint", "-bp", action="store_true",
                        help="Generate a complete Game Feel Blueprint for the product/feature query")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name for Blueprint")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Blueprint output format")
    parser.add_argument("--persist", action="store_true", help="Persist Blueprint to game-feel/<project-slug>/MASTER.md")
    parser.add_argument("--component", "-c", type=str, default=None, help="Also create component override in game-feel/<slug>/components/")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Target project directory for --persist")
    parser.add_argument("--force", action="store_true", help="Overwrite existing MASTER.md when persisting")

    # Sensory Dials (1-10)
    parser.add_argument("--juice", type=int, choices=range(1, 11), metavar="1-10",
                        help="JUICE INTENSITY dial (1=subliminal/crisp, 5=balanced spring, 10=expressive/gamified)")
    parser.add_argument("--forgiveness", type=int, choices=range(1, 11), metavar="1-10",
                        help="FORGIVENESS dial (1=standard, 6=150ms Coyote Time + 8px hitbox, 10=maximum assist)")
    parser.add_argument("--audio", type=int, choices=range(1, 11), metavar="1-10",
                        help="AUDIO/HAPTICS dial (1=silent/haptic-only, 5=subtle switch ticks, 10=full procedural synth)")

    args = parser.parse_args()

    # 1. Audit Mode
    if args.audit:
        report = audit_codebase(args.audit, max_opportunities=args.max_results if args.max_results != MAX_RESULTS else 15)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(format_audit_report(report))
        return

    if not args.query:
        parser.error("A search `query` is required unless `--audit <path>` is passed.")

    # 2. Blueprint Mode
    if args.blueprint:
        res = generate_blueprint(
            query=args.query,
            project_name=args.project_name,
            output_format=args.format,
            persist=args.persist,
            component=args.component,
            output_dir=args.output_dir,
            juice=args.juice,
            forgiveness=args.forgiveness,
            audio=args.audio,
            force=args.force,
        )
        if args.json:
            print(json.dumps({"blueprint": res["blueprint"], "persistence": res["persistence"]}, indent=2, ensure_ascii=False))
        else:
            print(res["text"])
            if args.persist and res.get("persistence"):
                p = res["persistence"]
                print("\n" + "=" * 68)
                if p.get("status") == "skipped_exists":
                    print(f"⚠️  {p.get('message')}")
                else:
                    print(f"✅ Game Feel Blueprint persisted to: {p.get('design_system_dir')}")
                    for cf in p.get("created_files", []):
                        print(f"   📄 {cf}")
                print("=" * 68)
        return

    # 3. Stack Mode
    if args.stack:
        res = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(format_search_output(res, full=args.full))
        return

    # 4. Domain Search Mode
    res = search(args.query, args.domain, args.max_results)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(format_search_output(res, full=args.full))


if __name__ == "__main__":
    main()
