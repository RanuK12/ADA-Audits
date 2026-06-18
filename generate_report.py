import json
from datetime import datetime

def generate_report(data):
    report = []
    report.append(f"# Auditoría de Seguridad: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")
    
    report.append("\n## Hallazgos Detallados")
    report.append("| Hallazgo | Severidad | Impacto |")
    report.append("| --- | --- | --- |")
    
    for item in data['findings']:
        report.append(f"| {item['issue']} | {item['severity']} | {item['impact']} |")
    
    report.append("\n## Recomendaciones")
    for rec in data['recommendations']:
        report.append(f"- {rec}")
    
    return "\n".join(report)

def main():
    sample_data = {
        "client_name": "Garycio",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": "Se identificaron vulnerabilidades críticas en la gestión de secretos y accesos SSH.",
        "findings": [
            {"issue": "Secretos en .env", "severity": "Critical", "impact": "Acceso total a DB y API."},
            {"issue": "Password SSH débil", "severity": "Critical", "impact": "Acceso no autorizado al servidor."}
        ],
        "recommendations": [
            "Mover secretos a un Vault.",
            "Desactivar login por password y usar llaves SSH.",
            "Rotar todos los tokens inmediatamente."
        ]
    }
    
    report_content = generate_report(sample_data)
    with open("sample_audit_report.md", "w") as f:
        f.write(report_content)
    print("Reporte generado en sample_audit_report.md")

if __name__ == "__main__":
    main()
