#!/usr/bin/env python3
"""Entry point for `python -m scripts`.

Provides a unified CLI to run ADA audit tools.
Usage:
  python -m scripts scan <axe-json-file>
  python -m scripts version
"""

import json
import sys

from scripts import __version__
from scripts.compliance_score import calc_score, get_criteria_status, risk_info


def cmd_version():
    print(f"ada-audits v{__version__}")


def cmd_scan(args):
    if not args:
        print("Usage: python -m scripts scan <axe-json-file>", file=sys.stderr)
        sys.exit(1)

    path = args[0]
    if path == "-":
        data = json.load(sys.stdin)
    else:
        with open(path) as f:
            data = json.load(f)

    if isinstance(data, list) and data:
        data = data[0]

    violations = data.get("violations", [])
    score = calc_score(violations)
    criteria = get_criteria_status(violations)

    buckets = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
    for v in violations:
        buckets[v.get("impact", "minor")] += 1

    legal_risk, recommendation = risk_info(score)

    output = {
        "url": data.get("url", "unknown"),
        "wcag_compliance_score": score,
        "total_violations": len(violations),
        "by_severity": buckets,
        "criteria_violated": len(criteria),
        "legal_risk": legal_risk,
        "recommendation": recommendation,
        "violated_criteria": [
            {"criterion": k, "violations": v["count"], "severity": v["worst"]}
            for k, v in sorted(criteria.items())
        ],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if sys.argv[1:] and sys.argv[1] in ("-h", "--help") else 1)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == "version":
        cmd_version()
    elif cmd == "scan":
        cmd_scan(rest)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
