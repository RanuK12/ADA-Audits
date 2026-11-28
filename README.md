# ADA-Audits

Auditorías de accesibilidad WCAG 2.1 AA para PyMEs.

El informe **vende solo**: cada hallazgo trae su impacto en plata o riesgo legal explicado en una línea, una comparativa antes/después, y un CTA para contratar el fix.

---

## Qué hace el proyecto

`generate_report.py` lee los resultados de una auditoría de accesibilidad y produce un informe listo para enviar al cliente. El informe no solo lista errores: traduce cada hallazgo en **dinero perdido** o **exposición legal**, muestra el antes y el después de la página, y cierra con una llamada a la acción para que el cliente contrate la corrección.

Está pensado para que una PyME lo reciba, entienda cuánto le está costando no ser accesible, y quiera pagar el fix.

---

## Cómo se genera un informe

```
python3 generate_report.py <archivo_de_auditoria.json>
```

### Archivo de entrada (ejemplo)

El JSON debe contener los hallazgos de accesibilidad (regla WCAG, elemento, descripción, página afectada):

```json
{
  "sitio": "ejemplo.com",
  "fecha": "2026-11-28",
  "hallazgos": [
    {
      "rule_id": "color-contrast",
      "nivel_wcag": "1.4.3",
      "elemento": "botón de compra",
      "descripcion": "El botón 'Comprar' no tiene suficiente contraste de color.",
      "pagina": "/carrito",
      "impacto_economico": "usuarios con baja visión no pueden completar la compra → pérdida estimada de ventas",
      "riesgo_legal": "incumplimiento WCAG 2.1 AA → posible demanda por accesibilidad",
      "fix": "ajustar contraste a 4.5:1",
      "antes": "captura_antes_carrito.png",
      "despues": "captura_despues_carrito.png",
      "cta": "Contratar el fix del botón de compra — $150"
    }
  ]
}
```

### Qué incluye el informe generado

- Resumen ejecutivo con los hallazgos más críticos
- **Impacto económico total** del sitio (pérdida estimada por inaccesibilidad)
- **Comparativa visual antes/después** de las páginas clave
- Cada hallazgo con: descripción, impacto en plata o riesgo legal (una línea), recomendación de fix y CTA
- **CTA final** para contactar a Emilio y contratar la corrección

---

## Ejemplo de informe (hallazgo)

> **Falta de contraste en botones de compra** — WCAG 1.4.3  
> Impacto: usuarios con baja visión no pueden completar la compra → pérdida estimada de ventas.  
> Riesgo legal: incumplimiento WCAG 2.1 AA → posible demanda por accesibilidad.  
> Fix: ajustar contraste a 4.5:1.  
> [CTA: Contratar el fix]

---

## CTA

¿Tenés una PyME y querés saber cuánto te está costando no ser accesible? Contactá a Emilio para contratar una auditoría y recibir el informe de venta.
