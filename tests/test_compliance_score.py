import pytest
from scripts.compliance_score import calc_score

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