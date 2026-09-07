"""Impact mapping for ADA audit findings.

Maps axe-core rule IDs to business impact statements and CTAs.
"""

IMPACT_MAP = {
    "color-contrast": {
        "impacto": "Mejora legibilidad para usuarios con baja visión o daltonismo, aumentando el tiempo en página y reduciendo la tasa de rebote.",
        "cta": "Contratar el fix de contraste de colores"
    },
    "image-alt": {
        "impacto": "Los usuarios de lectores de pantalla pueden entender el contenido de las imágenes, mejorando la accesibilidad y el SEO.",
        "cta": "Contratar el fix de texto alternativo para imágenes"
    },
    "label": {
        "impacto": "Los usuarios de lectores de pantalla pueden identificar el propósito de los campos de formulario, reduciendo errores y abandonos.",
        "cta": "Contratar el fix de etiquetas de formulario"
    },
    "link-name": {
        "impacto": "Los usuarios de lectores de pantalla entienden el destino de los enlaces, mejorando la navegación y reduciendo la confusión.",
        "cta": "Contratar el fix de nombres de enlaces descriptivos"
    },
    "button-name": {
        "impacto": "Los usuarios de lectores de pantalla saben qué hacen los botones, aumentando las conversiones en llamadas a la acción.",
        "cta": "Contratar el fix de nombres de botones accesibles"
    },
    "html-has-lang": {
        "impacto": "Los navegadores y lectores de pantalla pronuncian el contenido correctamente, mejorando la comprensión para usuarios internacionales.",
        "cta": "Contratar el fix de idioma de la página"
    },
    "document-title": {
        "impacto": "Los usuarios pueden identificar la página en pestañas y historial, mejorando la usabilidad y el SEO.",
        "cta": "Contratar el fix de título de documento"
    },
    "list": {
        "impacto": "Los usuarios de lectores de pantalla entienden la estructura de listas, mejorando la comprensión de contenido complejo.",
        "cta": "Contratar el fix de estructura de listas"
    },
    "region": {
        "impacto": "Los usuarios de lectores de pantalla pueden navegar por secciones de la página, mejorando la eficiencia y reduciendo la fatiga.",
        "cta": "Contratar el fix de landmarks ARIA"
    },
    "aria-required-attr": {
        "impacto": "Los usuarios de lectores de pantalla saben qué campos son obligatorios, reduciendo errores en formularios y abandonos.",
        "cta": "Contratar el fix de atributos ARIA requeridos"
    }
}

def get_impact_and_cta(rule_id):
    """Get impact statement and CTA for a given rule ID.
    
    Args:
        rule_id (str): The axe-core rule ID.
        
    Returns:
        tuple: (impact_statement, cta_string)
    """
    # Normalize rule_id to lowercase for matching
    rule_id_lower = rule_id.lower().strip()
    
    # Try exact match first
    if rule_id_lower in IMPACT_MAP:
        return IMPACT_MAP[rule_id_lower]["impacto"], IMPACT_MAP[rule_id_lower]["cta"]
    
    # Try partial matches for common variations
    for key, value in IMPACT_MAP.items():
        if key in rule_id_lower or rule_id_lower in key:
            return value["impacto"], value["cta"]
    
    # Fallback for unknown rules
    impacto_fallback = "Mejora accesibilidad y cumplimiento WCAG, reduciendo riesgo legal y mejorando experiencia para usuarios con discapacidad."
    cta_fallback = "Contratar el fix de accesibilidad"
    return impacto_fallback, cta_fallback