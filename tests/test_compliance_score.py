from scripts.compliance_score import calc_score, get_criteria_status, risk_info, tag_to_criterion


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
    # wcag111 → 1.1.1; wcag2a → 2.0.1 (principle 2, no sub-guide → defaults)
    assert "1.1.1" in result
    assert result["1.1.1"]["count"] == 1
    assert result["1.1.1"]["worst"] == "critical"

def test_get_criteria_status_multiple():
    violations = [
        {"tags": ["wcag111"], "impact": "critical"},
        {"tags": ["wcag111"], "impact": "serious"},
        {"tags": ["wcag244"], "impact": "minor"},
    ]
    result = get_criteria_status(violations)
    # wcag111 → 1.1.1, wcag244 → 2.4.4
    assert result["1.1.1"]["count"] == 2
    assert result["1.1.1"]["worst"] == "critical"
    assert result["2.4.4"]["count"] == 1
    assert result["2.4.4"]["worst"] == "minor"

# ── tag_to_criterion ──────────────────────────────────────────────────

def test_tag_to_criterion_wcag111():
    """wcag111 → 1.1.1 (Non-text Content)"""
    assert tag_to_criterion("wcag111") == "1.1.1"

def test_tag_to_criterion_wcag244():
    """wcag244 → 2.4.4 (Link Purpose)"""
    assert tag_to_criterion("wcag244") == "2.4.4"

def test_tag_to_criterion_wcag_with_level_aa():
    """wcag21aa → 2.1.1 (ignores trailing 'aa')"""
    assert tag_to_criterion("wcag21aa") == "2.1.1"

def test_tag_to_criterion_wcag_with_level_aaa():
    """wcag21aaa → 2.1.1 (ignores trailing 'aaa')"""
    assert tag_to_criterion("wcag21aaa") == "2.1.1"

def test_tag_to_criterion_wcag_with_three_level_aa():
    """wcag111aa → 1.1.1 (trailing 'aa' ignored)"""
    assert tag_to_criterion("wcag111aa") == "1.1.1"

def test_tag_to_criterion_wcag_principle_only():
    """wcag21 → 2.1.1 (no criterion number, defaults to 1)"""
    assert tag_to_criterion("wcag21") == "2.1.1"

def test_tag_to_criterion_wcag_principle_single_digit_returns_tag():
    """wcag1 (solo 1 dígito, no es tag axe válido) devuelve el tag original"""
    assert tag_to_criterion("wcag1") == "wcag1"

def test_tag_to_criterion_non_wcag_tag():
    """Non-wcag tags pasan sin cambios"""
    assert tag_to_criterion("best-practice") == "best-practice"
    assert tag_to_criterion("section508") == "section508"
    assert tag_to_criterion("cat.aria") == "cat.aria"

def test_tag_to_criterion_empty_rest():
    """wcag solo (sin dígitos) devuelve el tag original"""
    assert tag_to_criterion("wcag") == "wcag"

def test_tag_to_criterion_wcag412():
    """wcag412 → 4.1.2 (Name, Role, Value)"""
    assert tag_to_criterion("wcag412") == "4.1.2"

def test_tag_to_criterion_wcag131():
    """wcag131 → 1.3.1 (Info and Relationships)"""
    assert tag_to_criterion("wcag131") == "1.3.1"

def test_tag_to_criterion_wcag251():
    """wcag251 → 2.5.1 (Pointer Gestures)"""
    assert tag_to_criterion("wcag251") == "2.5.1"

def test_tag_to_criterion_wcag413():
    """wcag413 → 4.1.3 (Status Messages)"""
    assert tag_to_criterion("wcag413") == "4.1.3"

def test_tag_to_criterion_wcag143():
    """wcag143 → 1.4.3 (Contrast Minimum)"""
    assert tag_to_criterion("wcag143") == "1.4.3"

def test_tag_to_criterion_wcag2410():
    """wcag2410 → 2.4.10 (Section Headings)"""
    assert tag_to_criterion("wcag2410") == "2.4.10"

def test_tag_to_criterion_wcag2410_aa():
    """wcag2410aa → 2.4.10 (with level suffix)"""
    assert tag_to_criterion("wcag2410aa") == "2.4.10"

# ── get_criteria_status (existing) ────────────────────────────────────

def test_get_criteria_status_ignores_best():
    violations = [
        {"tags": ["wcag111", "wcag21aa", "best-practice"], "impact": "critical"}
    ]
    result = get_criteria_status(violations)
    # "best-practice" should be ignored
    assert "best-practice" not in result
    # wcag21aa → 2.1.1 should be included
    assert "2.1.1" in result
    assert "1.1.1" in result
