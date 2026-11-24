IMPACT_MAP = {
    "missing_alt": {
        "cost": "$200–$500",
        "risk": "Posible demanda por inaccesibilidad",
        "cost_line": "Cada imagen sin texto alternativo es un cliente que no puede comprar: corregirlas cuesta entre $200 y $500 y recuperás ventas que hoy se te escapan.",
        "risk_line": "Riesgo legal: incumplís WCAG 2.1 y expón tu web a demandas por discriminación digital.",
    },
    "low_contrast": {
        "cost": "$150–$300",
        "risk": "Deserción de usuarios",
        "cost_line": "El bajo contraste hace que un 21% de los usuarios abandone antes de completar una acción: arreglarlo cuesta $150–$300 y frena esa fuga.",
        "risk_line": "Riesgo legal: incumplís el criterio de contraste de WCAG 2.1, base de muchas demandas de accesibilidad.",
    },
    "keyboard_nav": {
        "cost": "$300–$600",
        "risk": "Exclusión de usuarios con discapacidad motriz",
        "cost_line": "Sin navegación por teclado excluís a usuarios que no pueden usar el mouse: la corrección cuesta $300–$600 y te abre ese segmento de mercado.",
        "risk_line": "Riesgo legal: la falta de navegación por teclado viola WCAG 2.1 y expone a demandas por inaccesibilidad.",
    },
    "aria_label": {
        "cost": "$100–$250",
        "risk": "Confusión en lectores de pantalla",
        "cost_line": "Etiquetas ARIA faltantes confunden a lectores de pantalla y pierdes compradores: corregirlas cuesta $100–$250 y mejora la experiencia de compra.",
        "risk_line": "Riesgo legal: sin ARIA los usuarios de lectores de pantalla no pueden navegar, incumpliendo WCAG 2.1.",
    },
    "form_label": {
        "cost": "$150–$400",
        "risk": "Errores en envío de formularios",
        "cost_line": "Formularios sin etiquetas generan abandono y errores de envío: arreglarlos cuesta $150–$400 y recuperás conversiones perdidas.",
        "risk_line": "Riesgo legal: formularios inaccesibles violan WCAG 2.1 y son blanco frecuente de demandas.",
    },
    "heading_structure": {
        "cost": "$100–$200",
        "risk": "Mala experiencia de navegación",
        "cost_line": "Una jerarquía de títulos desordenada dificulta la navegación y el SEO: reordenarla cuesta $100–$200 y mejora el posicionamiento en Google.",
        "risk_line": "Riesgo legal: la estructura de encabezados es requisito de WCAG 2.1; su ausencia expone a reclamos de accesibilidad.",
    },
}

DEFAULT_IMPACT = {
    "cost": "Consultá presupuesto",
    "risk": "Riesgo de incumplimiento de WCAG 2.1",
    "cost_line": "Cada barrera de accesibilidad es una venta que se te escapa y un riesgo legal que podés evitar hoy mismo.",
    "risk_line": "Riesgo legal: incumplir WCAG 2.1 expone tu web a demandas por discriminación digital.",
}
