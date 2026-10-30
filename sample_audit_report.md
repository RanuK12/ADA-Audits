# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-10-30
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## 💰 Impacto Económico Total
- **Pérdida estimada mensual:** $350.00
- **Ahorro anual potencial:** $4,200.00
- **Inversión estimada en fixes:** $450
- **ROI estimado:** 1.3 meses para recuperar la inversión
- **ROI anual:** 833%

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto Económico | Riesgo Legal | Explicación |
| --- | --- | --- | --- | --- |
| Contraste bajo en botón de compra | High | $50.00 | bajo | Costo estimado: $50.00/mes, riesgo legal bajo - Pérdida de conversión por falta de contraste adecuado |
| Imágenes de producto sin alt text | Medium | $100.00 | medio | Costo estimado: $100.00/mes, riesgo legal medio - Pérdida de ventas y riesgo de demanda por imágenes sin texto alternativo |
| Menú de navegación no operable por teclado | Critical | $200.00 | alto | Costo estimado: $200.00/mes, riesgo legal alto - Usuarios sin mouse no pueden navegar, riesgo de demanda ADA |

### Contraste bajo en botón de compra
**Impacto en el negocio:** –12% conversión mobile / demanda ADA Title III
**Explicación de impacto:** Costo estimado: $50.00/mes, riesgo legal bajo - Pérdida de conversión por falta de contraste adecuado
**Antes → Después**
**Antes:** `<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>` (contraste 2.1:1)
**Después:** `<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>` (contraste 4.5:1)
Contratar fix: [Contacto](mailto:emilio@ranuk.dev)
![Antes/Después](before_after_low_contrast.png)

### Imágenes de producto sin alt text
**Impacto en el negocio:** Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
**Explicación de impacto:** Costo estimado: $100.00/mes, riesgo legal medio - Pérdida de ventas y riesgo de demanda por imágenes sin texto alternativo
**Antes → Después**
**Antes:** `<img src="producto.jpg">`
**Después:** `<img src="producto.jpg" alt="Zapatillas running azul">`
Contratar fix: [Contacto](mailto:emilio@ranuk.dev)
![Antes/Después](before_after_missing_alt.png)

### Menú de navegación no operable por teclado
**Impacto en el negocio:** Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA
**Explicación de impacto:** Costo estimado: $200.00/mes, riesgo legal alto - Usuarios sin mouse no pueden navegar, riesgo de demanda ADA
**Antes → Después**
**Antes:** `<div class="menu" onclick="toggleMenu()">` (sin `tabindex` ni `role`)
**Después:** `<nav aria-label="Principal"><ul role="menubar">…</ul></nav>` con manejo de teclado
Contratar fix: [Contacto](mailto:emilio@ranuk.dev)
![Antes/Después](before_after_keyboard_trap.png)

## Recomendaciones
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

💡 Arreglamos esto por vos — [contratá el fix](mailto:emilio@ranuk.dev)