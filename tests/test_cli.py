"""Tests for the CLI entry point (__main__.py)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run the CLI as `python -m scripts ...` and return result."""
    return subprocess.run(
        [sys.executable, "-m", "scripts", *args],
        capture_output=True,
        text=True,
        cwd=SCRIPTS_DIR.parent,
    )


SAMPLE_VIOLATIONS = {
    "url": "https://example.com",
    "violations": [
        {"id": "color-contrast", "impact": "serious", "tags": ["wcag143", "wcag2aa"]},
        {"id": "image-alt", "impact": "critical", "tags": ["wcag111"]},
        {"id": "link-name", "impact": "minor", "tags": ["wcag244", "wcag2a"]},
    ],
}


# ── version ───────────────────────────────────────────────────────────


def test_cli_version():
    result = run_cli("version")
    assert result.returncode == 0
    assert "ada-audits v" in result.stdout


# ── scan ──────────────────────────────────────────────────────────────


def test_cli_scan_stdin():
    """Scan reads JSON from stdin when '-' is passed."""
    result = subprocess.run(
        [sys.executable, "-m", "scripts", "scan", "-"],
        input=json.dumps(SAMPLE_VIOLATIONS),
        capture_output=True,
        text=True,
        cwd=SCRIPTS_DIR.parent,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["url"] == "https://example.com"
    assert data["total_violations"] == 3
    assert data["wcag_compliance_score"] == 87  # 100 - 8(crit) - 4(serious) - 1(minor)
    assert data["legal_risk"] == "LOW"


def test_cli_scan_file(tmp_path):
    """Scan reads JSON from a file."""
    f = tmp_path / "audit.json"
    f.write_text(json.dumps(SAMPLE_VIOLATIONS))
    result = run_cli("scan", str(f))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["total_violations"] == 3
    assert data["wcag_compliance_score"] == 87


def test_cli_scan_empty_violations(tmp_path):
    """No violations → score 100."""
    f = tmp_path / "clean.json"
    f.write_text(json.dumps({"url": "https://clean.site", "violations": []}))
    result = run_cli("scan", str(f))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["total_violations"] == 0
    assert data["wcag_compliance_score"] == 100
    assert data["legal_risk"] == "LOW"


def test_cli_scan_critical_score_floor(tmp_path):
    """Many critical violations floor at 0."""
    violations = [{"impact": "critical"}] * 20
    f = tmp_path / "critical.json"
    f.write_text(json.dumps({"violations": violations}))
    result = run_cli("scan", str(f))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["wcag_compliance_score"] == 0
    assert data["legal_risk"] == "CRITICAL"


def test_cli_scan_list_input(tmp_path):
    """Accepts a list of results (axe multi-page mode), uses first."""
    f = tmp_path / "multi.json"
    f.write_text(json.dumps([SAMPLE_VIOLATIONS, {"url": "https://other.com"}]))
    result = run_cli("scan", str(f))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["url"] == "https://example.com"


# ── help / error ──────────────────────────────────────────────────────


def test_cli_no_args():
    result = run_cli()
    assert result.returncode == 1
    assert "Usage" in result.stdout or "Usage" in result.stderr


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0


def test_cli_unknown_command():
    result = run_cli("unknown")
    assert result.returncode == 1
    assert "Unknown command" in result.stderr


def test_cli_scan_no_file():
    """scan without file arg should exit with error."""
    result = run_cli("scan")
    assert result.returncode == 1
    assert "Usage" in result.stderr
