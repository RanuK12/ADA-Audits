"""Tests para render_html_report.py"""
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Importar después de ajustar sys.path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from render_html_report import render


SAMPLE_DATA = {
    "company": "TestCorp",
    "url": "https://testcorp.com",
    "date": "2026-07-30",
    "score": 52,
    "executive_summary": "Resumen ejecutivo de prueba.",
    "risk_description": "Riesgo moderado-alto.",
    "methodology": "axe-core + manual.",
    "findings": {
        "Crítico": [
            {"id": "C1", "wcag_criterion": "1.1.1", "description": "Sin alt text",
             "nodes_affected": 5, "effort": "1h"}
        ],
        "Alto": [
            {"id": "A1", "wcag_criterion": "1.4.3", "description": "Contraste bajo",
             "nodes_affected": 3, "effort": "30min"}
        ],
        "Medio": []
    },
    "top3_issues": [
        {"title": "Issue 1", "description": "Desc 1", "wcag_criterion": "1.1.1",
         "effort": "1h", "risk_class": "critical"}
    ],
    "remediation_phases": [
        {"title": "Fase 1", "tasks": ["Tarea 1"], "deliverable": "0 críticos", "risk_class": "critical"}
    ],
    "price": 1500,
    "pricing_note": "Incluye soporte 30 días.",
    "consequences": "<p>Riesgo legal.</p>",
    "compliance_table": [
        {"criterion": "1.1.1", "status": "Falla", "violations": 5, "badge_class": "badge-critical"}
    ]
}


def test_score_class_critical():
    """Score < 50 → sc-crit, ALTO."""
    data = {**SAMPLE_DATA, "score": 30}
    render(data, "/dev/null")
    assert data["score_class"] == "sc-crit"
    assert data["risk_level"] == "ALTO"


def test_score_class_serious():
    """Score 50-69 → sc-serious, MEDIO."""
    data = {**SAMPLE_DATA, "score": 65}
    render(data, "/dev/null")
    assert data["score_class"] == "sc-serious"
    assert data["risk_level"] == "MEDIO"


def test_score_class_moderate():
    """Score 70-89 → sc-mod, MODERADO."""
    data = {**SAMPLE_DATA, "score": 80}
    render(data, "/dev/null")
    assert data["score_class"] == "sc-mod"
    assert data["risk_level"] == "MODERADO"


def test_score_class_good():
    """Score >= 90 → sc-good, BAJO."""
    data = {**SAMPLE_DATA, "score": 95}
    render(data, "/dev/null")
    assert data["score_class"] == "sc-good"
    assert data["risk_level"] == "BAJO"


def test_counts():
    """Verifica conteo de findings por severidad."""
    data = {**SAMPLE_DATA}
    render(data, "/dev/null")
    assert data["critical_count"] == 1
    assert data["serious_count"] == 1
    assert data["moderate_count"] == 0
    assert data["total_count"] == 2


def test_generates_valid_pdf():
    """Verifica que se genera un PDF válido con datos reales."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        pdf_path = f.name
    try:
        render(SAMPLE_DATA, pdf_path)
        assert os.path.getsize(pdf_path) > 1000
        with open(pdf_path, "rb") as f:
            assert f.read(5) == b"%PDF-"
    finally:
        os.unlink(pdf_path)
        html_path = pdf_path.replace(".pdf", ".html")
        if os.path.exists(html_path):
            os.unlink(html_path)


def test_css_path_is_set():
    """Verifica que se setea css_path."""
    data = {**SAMPLE_DATA}
    render(data, "/dev/null")
    assert "css_path" in data
    assert data["css_path"].endswith("pdf-style.css")