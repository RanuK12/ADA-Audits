import json

IMPACT_MAP = {
    "missing_alt": {"cost": "$200–$500", "risk": "Posible demanda por inaccesibilidad"},
    "low_contrast": {"cost": "$150–$300", "risk": "Deserción de usuarios"},
    "keyboard_nav": {"cost": "$300–$600", "risk": "Exclusión de usuarios con discapacidad motriz"},
    "aria_label": {"cost": "$100–$250", "risk": "Confusión en lectores de pantalla"},
    "form_label": {"cost": "$150–$400", "risk": "Errores en envío de formularios"},
    "heading_structure": {"cost": "$100–$200", "risk": "Mala experiencia de navegación"},
}

def estimate_impact(issue_type: str, severity: str = "medium") -> dict:
    """Estima el impacto económico y legal de un hallazgo de accesibilidad.
    
    Args:
        issue_type: Tipo de hallazgo (ej: 'missing_alt', 'low_contrast').
        severity: Severidad del hallazgo (default: 'medium').
    
    Returns:
        dict: {"cost": "$X–$Y", "risk": "Riesgo legal"}
    """
    issue_key = issue_type
    if issue_key not in IMPACT_MAP:
        raise ValueError(f"Issue type '{issue_key}' not found in impact map.")
    
    return IMPACT_MAP[issue_key]

if __name__ == "__main__":
    print(estimate_impact("missing_alt"))