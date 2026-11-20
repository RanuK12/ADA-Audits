# ADA-Audits

Auditorías de accesibilidad WCAG 2.1 AA para PyMEs.

El informe genera venta: cada hallazgo trae su impacto en plata o riesgo legal explicado en una línea, una comparativa antes/después, y un CTA para contratar el fix.

## Qué hace el proyecto

`generate_report.py` lee los resultados de una auditoría de accesibilidad y produce un informe listo para enviar al cliente. El informe no solo lista errores: traduce cada hallazgo en dinero perdido o exposición legal, muestra el antes y el después de la página, y cierra con una llamada a la acción para que el cliente contrate la corrección.

## Cómo se genera un informe

```
python3 generate_report.py <archivo_de_auditoria.json>
```

El archivo de entrada debe contener los hallazgos de accesibilidad (nivel WCAG, elemento, descripción, página afectada). El script genera un PDF con:

- Resumen ejecutivo con los hallazgos más críticos
- Impacto económico total del sitio (pérdida estimada por inaccesibilidad)
- Comparativa visual antes/después de las páginas clave
- Cada hallazgo con: descripción, impacto en plata o riesgo legal (una línea), y recomendación de fix
- CTA final para contactar a Emilio y contratar la corrección

## Ejemplo de informe

Cada hallazgo se presenta así:

> **Falta de contraste en botones de compra** — WCAG 1.4.3  
> Impacto: usuarios con baja visión no pueden completar la compra → pérdida estimada de ventas.  
> Fix: ajustar contraste a 4.5:1.  
> [CTA: Contratar el fix]

## CTA

¿Tenés una PyME y querés saber cuánto te está costando no ser accesible? Contactá a Emilio para contratar una auditoría y el informe de venta.
