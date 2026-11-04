#!/usr/bin/env python3
"""Ranuk Cloud & DevSecOps Security Auditor (powered by ittcsecscan).

Runs read-only, local-first security posture audits across:
- MCP Servers & AI Agent configurations (AI Guard)
- GitHub Organizations & Repositories
- Cloud Providers (AWS, Azure, GCP)

Outputs deliverables in PDF, DOCX, HTML, SARIF, and JSON.

Usage:
    python cloud-security-audit.py --mcp path/to/mcp.json
    python cloud-security-audit.py --github [--budget 30]
    python cloud-security-audit.py --provider aws
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_PASSPHRASE = os.environ.get("ITTCSECSCAN_PASSPHRASE", "ranuk-ittcsecscan-master-2026")
DEFAULT_BIN = shutil.which("ittcsecscan") or "/opt/homebrew/bin/ittcsecscan"
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUT = BASE_DIR / "entregables" / "security"

def resolve_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return None

def run_scan(provider, target_path=None, budget=0, out_dir=DEFAULT_OUT):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["ITTCSECSCAN_PASSPHRASE"] = DEFAULT_PASSPHRASE

    if provider == "mcp":
        if not target_path:
            raise ValueError("Target path required for provider 'mcp'")
        env["MCP_CONFIG_FILE"] = str(Path(target_path).resolve())
    elif provider == "github":
        token = resolve_github_token()
        if token:
            env["GITHUB_TOKEN"] = token
        else:
            print("Warning: GITHUB_TOKEN not found and gh auth token failed", file=sys.stderr)

    cmd = [
        DEFAULT_BIN,
        "scan",
        "--create",
        "--provider", provider,
        "--report-dir", str(out_dir),
    ]
    if budget > 0:
        cmd.extend(["--budget", str(budget)])

    res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    report_json_path = out_dir / "report.json"
    data = {}
    if report_json_path.exists():
        try:
            with open(report_json_path) as f:
                data = json.load(f)
        except Exception as e:
            data = {"error": f"Failed to read report.json: {e}"}

    summary = {
        "provider": provider,
        "target": target_path or provider,
        "exit_code": res.returncode,
        "raw_stdout": res.stdout.strip(),
        "deliverables": {
            "json": str(out_dir / "report.json") if (out_dir / "report.json").exists() else None,
            "pdf": str(out_dir / "report.pdf") if (out_dir / "report.pdf").exists() else None,
            "html": str(out_dir / "report.html") if (out_dir / "report.html").exists() else None,
            "docx": str(out_dir / "report.docx") if (out_dir / "report.docx").exists() else None,
            "sarif": str(out_dir / "report.sarif.json") if (out_dir / "report.sarif.json").exists() else None,
        },
        "findings_count": len(data.get("findings", [])),
        "attack_paths_count": len(data.get("paths", [])),
        "coverage_complete": data.get("coverage", {}).get("complete", False),
    }
    return summary

def main():
    parser = argparse.ArgumentParser(description="Ranuk Cloud & DevSecOps Security Auditor")
    parser.add_argument("--mcp", type=str, help="Path to MCP config JSON file to scan")
    parser.add_argument("--github", action="store_true", help="Scan GitHub organization/repositories")
    parser.add_argument("--provider", type=str, default="mcp", help="Provider name (mcp, github, aws, azure, gcp)")
    parser.add_argument("--budget", type=int, default=0, help="API call budget cap (0 = unlimited)")
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT), help="Output directory for reports")
    parser.add_argument("--json", action="store_true", help="Output summary in JSON format")

    args = parser.parse_args()

    if args.mcp:
        provider = "mcp"
        target = args.mcp
    elif args.github:
        provider = "github"
        target = None
    else:
        provider = args.provider
        target = None

    summary = run_scan(provider=provider, target_path=target, budget=args.budget, out_dir=args.out)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("=== Ranuk Security Audit Summary ===")
        print(f"Provider:    {summary['provider']}")
        print(f"Target:      {summary['target']}")
        print(f"Coverage:    {'Complete' if summary['coverage_complete'] else 'Partial/Gaps'}")
        print(f"Findings:    {summary['findings_count']}")
        print(f"Paths:       {summary['attack_paths_count']}")
        print("Deliverables:")
        for fmt, p in summary["deliverables"].items():
            if p:
                print(f"  - {fmt.upper()}: {p}")

if __name__ == "__main__":
    main()
