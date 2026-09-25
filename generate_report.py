import json
from datetime import datetime

def generate_report(data):
    report = []
    report.append(f"# Auditoría de Accesibilidad WCAG: {data['client_name']}")
    report.append(f"**Fecha:** {data['date']}")
    report.append(f"**Estado:** Finalizado")
    report.append("\n## Resumen Ejecutivo")
    report.append(f"{data['summary']}")
    
    if data['findings']:
        report.append("\n## Hallazgos Detallados")
        report.append("| Hallazgo | Severidad | Impacto en el negocio | Impacto financiero estimado |")
        report.append("| --- | --- | --- | --- |")
        
        for item in data['findings']:
            # Estimar impacto financiero basado en severidad y tipo de hallazgo
            impacto_financiero = "No estimado"
            severidad = item.get('severity', '').lower()
            issue_texto = item.get('issue', '').lower()
            # Lógica simple de estimación financiera
            if 'contraste' in issue_texto or 'color' in issue_texto:
                impacto_financiero = "$500 - $2,000 (pérdida de conversiones)"
            elif 'navegación' in issue_texto or 'menu' in issue_texto or 'teclado' in issue_texto:
                impacto_financiero = "$1,000 - $5,000 (abandono de sitio)"
            elif 'formulario' in issue_texto or 'input' in issue_texto or 'alt text' in issue_texto or 'imagen' in issue_texto:
                impacto_financiero = "$1,500 - $3,000 (pérdida de leads/ventas)"
            elif 'encabezado' in issue_texto or 'heading' in issue_texto:
                impacto_financiero = "$400 - $1,800 (usabilidad y retención)"
            elif severidad in ['critical', 'high']:
                impacto_financiero = "$2,000 - $10,000 (riesgo legal y pérdida significativa)"
            elif severidad == 'medium':
                impacto_financiero = "$500 - $3,000 (mejora de experiencia y retención)"
            else:
                impacto_financiero = "$100 - $1,000 (mejora menor)"
            report.append(f"| {item['issue']} | {item['severity']} | {item['business_impact']} | {impacto_financiero} |")
        
        # Antes → Después sub‑sections
        for item in data['findings']:
            report.append(f"\n### {item['issue']}")
            report.append(f"**Impacto en el negocio:** {item['business_impact']}")
            
            # Línea de impacto económico/legal
            impacto_legal = _estimate_legal_impact(item)
            report.append(f"**⚖️ Impacto económico / riesgo legal:** {impacto_legal}")
            
            # Ejemplo visual simulado
            visual_example = _generate_visual_example(item)
            report.append(f"**🎨 Ejemplo visual de la corrección:**\n{visual_example}")
            
            report.append("**Antes → Después**")
            report.append(f"**Antes:** {item['before']}")
            report.append(f"**Después:** {item['after']}")
            
            # CTA por hallazgo
            cta = _generate_cta(item)
            report.append(f"**💡 Próximo paso:** {cta}")
    
    if data['recommendations']:
        report.append("\n## Recomendaciones")
        for rec in data['recommendations']:
            report.append(f"- {rec}")
    
    # CTA mejorado con estimado de precio y llamado a la acción más directo
    total_estimado = "Consultá nuestro presupuesto personalizado (ej: arreglos básicos desde $800, auditoría completa + fix desde $1500)"
    report.append(f"\n💡 **¿Listo para hacer tu sitio accesible y evitar demandas?**")
    report.append(f"Arreglamos estos problemas por vos. Presupuesto estimado: {total_estimado}.")
    report.append(f"👉 [Contratá el servicio de fix ahora](mailto:emilio@ranuk.dev?subject=Auditoría%20y%20Fix%20de%20Accesibilidad)")
    
    return "\n".join(report)

def _estimate_legal_impact(item):
    """Estima el impacto económico o riesgo legal basado en el hallazgo."""
    issue = item.get('issue', '').lower()
    severity = item.get('severity', '').lower()
    
    if 'contraste' in issue or 'color' in issue:
        return "Multas ADA hasta $4,000 + pérdida de conversiones por mala legibilidad"
    elif 'alt text' in issue or 'imagen' in issue:
        return "Riesgo de demanda por inaccessibilidad + pérdida de tráfico SEO y ventas"
    elif 'navegación' in issue or 'menú' in issue or 'teclado' in issue:
        return "Exclusión de usuarios con discapacidad motriz → abandono y posibles acciones legales"
    elif 'formulario' in issue or 'input' in issue:
        return "Imposibilidad de completar compras o leads → pérdida directa de ingresos"
    elif 'encabezado' in issue or 'heading' in issue:
        return "Mala estructura de contenido → confusión para usuarios de lectores de pantalla"
    elif severity == 'critical':
        return "Riesgo alto de demanda ADA + multas significativas por incumplimiento"
    elif severity == 'high':
        return "Impacto mediano-alto en accesibilidad y exposición legal"
    elif severity == 'medium':
        return "Mejora necesaria para evitar riesgos acumulativos y mejorar experiencia"
    else:
        return "Ajuste menor que contribuye al cumplimiento general y buena práctica"

def _generate_visual_example(item):
    """Genera un ejemplo visual simulado de cómo se vería la corrección."""
    issue = item.get('issue', '').lower()
    
    if 'contraste' in issue or 'color' in issue:
        return "Botón con colores ajustados para contraste mínimo 4.5:1 (ej: naranja oscuro sobre blanco)"
    elif 'alt text' in issue or 'imagen' in issue:
        return "Imagen con atributo alt descriptivo: alt='Zapatillas running azul'"
    elif 'navegación' in issue or 'menú' in issue or 'teclado' in issue:
        return "Menú con roles ARIA y tabindex para navegación completa por teclado"
    elif 'formulario' in issue or 'input' in issue:
        return "Formulario con labels asociados, placeholders apropiados y validación accesible"
    elif 'encabezado' in issue or 'heading' in issue:
        return "Jerarquía de encabezados correcta (H1 → H2 → H3) sin saltos de nivel"
    else:
        return "Elemento corregido según mejores prácticas WCAG 2.1"

def _generate_cta(item):
    """Genera una llamada a la acción específica para el hallazgo."""
    issue = item.get('issue', '').lower()
    
    if 'contraste' in issue or 'color' in issue:
        return "Ajustar colores en CSS/SCSS. Tiempo estimado: 10-15 minutos."
    elif 'alt text' in issue or 'imagen' in issue:
        return "Agregar texto alternativo descriptivo a todas las imágenes. Tiempo estimado: 5-10 minutos por imagen."
    elif 'navegación' in issue or 'menú' in issue or 'teclado' in issue:
        return "Implementar navegación por teclado con ARIA. Tiempo estimado: 20-30 minutos."
    elif 'formulario' in issue or 'input' in issue:
        return "Mejorar accesibilidad de formularios (labels, placeholders, validación). Tiempo estimado: 15-25 minutos."
    elif 'encabezado' in issue or 'heading' in issue:
        return "Corregir jerarquía de encabezados. Tiempo estimado: 5-10 minutos."
    else:
        return "Implementar corrección según recomendaciones WCAG. Tiempo estimado: variable."

def main():
    sample_data = {
        "client_name": "TiendaOnline Demo",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": "Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.",
        "findings": [
            {
                "issue": "Contraste bajo en botón de compra",
                "severity": "High",
                "business_impact": "–12% conversión mobile / demanda ADA Title III",
                "before": "`<button style=\"background: #FFA500; color: #FFFFFF;\">Comprar</button>` (contraste 2.1:1)",
                "after": "`<button style=\"background: #D2691E; color: #FFFFFF;\">Comprar</button>` (contraste 4.5:1)"
            },
            {
                "issue": "Imágenes de producto sin alt text",
                "severity": "Medium",
                "business_impact": "Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda",
                "before": "`<img src=\"producto.jpg\">`",
                "after": "`<img src=\"producto.jpg\" alt=\"Zapatillas running azul\">`"
            },
            {
                "issue": "Menú de navegación no operable por teclado",
                "severity": "Critical",
                "business_impact": "Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA",
                "before": "`<div class=\"menu\" onclick=\"toggleMenu()\">` (sin `tabindex` ni `role`)",
                "after": "`<nav aria-label=\"Principal\"><ul role=\"menubar\">…</ul></nav>` con manejo de teclado"
            }
        ],
        "recommendations": [
            "Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).",
            "Agregar texto alternativo descriptivo a todas las imágenes de producto.",
            "Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco."
        ]
    }
    
    report_content = generate_report(sample_data)
    with open("sample_audit_report.md", "w") as f:
        f.write(report_content)
    print("Reporte generado en sample_audit_report.md")

if __name__ == "__main__":
    main()
