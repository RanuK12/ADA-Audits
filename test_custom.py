import json
from generate_report import generate_report

custom_data = {
    "client_name": "Acme Corp",
    "date": "2026-09-07",
    "summary": "Test auditoría.",
    "findings": [
        {
            "issue": "Texto de contraste insuficiente",
            "severity": "Medium",
            "business_impact": "Baja legibilidad para usuarios con baja visión.",
            "before": "<p style=\"color:#lightgray\">Texto</p>",
            "after": "<p style=\"color:#darkgray\">Texto</p>"
        }
    ],
    "recommendations": [
        "Aumentar contraste de texto."
    ]
}

report = generate_report(custom_data)
print("=== REPORT ===")
print(report)
print("=== END ===")
# Quick checks
assert "Acme Corp" in report
assert "Texto de contraste insuficiente" in report
assert "Baja legibilidad" in report
assert "<p style=\"color:#lightgray\">Texto</p>" in report
assert "<p style=\"color:#darkgray\">Texto</p>" in report
print("All checks passed.")
