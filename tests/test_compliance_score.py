import pytest
from scripts.compliance_score import calc_score, get_criteria_status, risk_info

def test_calc_score_perfect_score():
    # Sin violaciones debería ser 100
    assert calc_score([]) == 100

def test_calc_score_critical_violation():
    # Una violación crítica resta 8 puntos
    violations = [{"impact": "critical"}]
    assert calc_score(violations) == 92

def test_calc_score_multiple_violations():
    # Varias violaciones con distintos pesos
    violations = [
        {"impact": "critical"},  # -8
        {"impact": "serious"},   # -4
        {"impact": "minor"}      # -1
    ]
    # 100 - 13 = 87
    assert calc_score(violations) == 87

def test_calc_score_score_floor():
    # Muchísimas críticas que deberían bajar a 0 (no negativo)
    violations = [{"impact": "critical"}] * 20  # 20 * 8 = 160 > 100
    assert calc_score(violations) == 0

def test_calc_score_score_ceiling():
    # Si no hay violaciones, nunca supera 100
    violations = [{"impact": "minor"}] * 5
    # 5 * 1 = 5 → 95
    assert calc_score(violations) == 95

def test_risk_info_critical():
    risk, rec = risk_info(20)
    assert risk == "CRITICAL"
    assert "Immediate" in rec

def test_risk_info_high():
    risk, rec = risk_info(50)
    assert risk == "HIGH"
    assert "Prompt" in rec

def test_risk_info_moderate():
    risk, rec = risk_info(70)
    assert risk == "MODERATE"
    assert "Improvements" in rec

def test_risk_info_low():
    risk, rec = risk_info(90)
    assert risk == "LOW"
    assert "Minor" in rec

def test_risk_info_boundaries():
    # score == 30 should be HIGH (not CRITICAL)
    risk, rec = risk_info(30)
    assert risk == "HIGH"
    # score == 60 should be MODERATE
    risk, rec = risk_info(60)
    assert risk == "MODERATE"
    # score == 80 should be LOW
    risk, rec = risk_info(80)
    assert risk == "LOW"

def test_get_criteria_status_empty():
    assert get_criteria_status([]) == {}

def test_get_criteria_status_single():
    violations = [
        {
            "tags": ["wcag2a", "wcag111"],
            "impact": "critical"
        }
    ]
    result = get_criteria_status(violations)
    assert "wcag111" in result
    assert result["wcag111"]["count"] == 1
    assert result["wcag111"]["worst"] == "critical"

def test_get_criteria_status_multiple():
    violations = [
        {"tags": ["wcag111"], "impact": "critical"},
        {"tags": ["wcag111"], "impact": "serious"},
        {"tags": ["wcag244"], "impact": "minor"},
    ]
    result = get_criteria_status(violations)
    assert result["wcag111"]["count"] == 2
    assert result["wcag111"]["worst"] == "critical"
    assert result["wcag244"]["count"] == 1
    assert result["wcag244"]["worst"] == "minor"

def test_get_criteria_status_ignores_best():
    violations = [
        {"tags": ["wcag111", "wcag21aa", "best-practice"], "impact": "critical"}
    ]
    result = get_criteria_status(violations)
    # "best-practice" should be ignored
    assert "best-practice" not in result
    # wcag21aa should be included
    assert "wcag21aa" in result
