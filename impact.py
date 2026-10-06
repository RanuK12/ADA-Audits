#!/usr/bin/env python3
import json
from utils.economic_impact import estimate_cost

# Carga la matriz de impacto desde un archivo JSON
def load_impact_matrix():
    with open('impact_matrix.json', 'r') as f:
        return json.load(f)

# Estima el impacto económico y legal para un hallazgo específico
def estimate_impact(wcag_level, severity, issue_type):
    impact_matrix = load_impact_matrix()
    
    # Obtener el costo estimado basado en el tipo de hallazgo y severidad
    cost = estimate_cost(issue_type, severity)
    
    # Obtener el riesgo legal basado en la severidad
    legal_risk = "bajo"
    if severity.lower() == "critical":
        legal_risk = "alto"
    elif severity.lower() == "high":
        legal_risk = "moderado"
    elif severity.lower() == "medium":
        legal_risk = "medio"
    
    return {
        "cost": cost,
        "legal_risk": legal_risk
    }

# Ejemplo de uso
if __name__ == "__main__":
    print(estimate_impact("WCAG2.1", "Medium", "missing_alt"))