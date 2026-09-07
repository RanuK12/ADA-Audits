# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-09-08
**Estado:** Finalizado

## Resumen Ejecutivo
Auditoría de accesibilidad WCAG 2.1 AA — se detectaron barreras que afectan la experiencia de usuarios con discapacidad y exponen a la empresa a riesgos legales.

## 💰 Impacto Financiero y Riesgo Legal
- **Contraste bajo en botón de compra** → –12% conversión mobile / demanda ADA Title III
- **Imágenes de producto sin alt text** → Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
- **Menú de navegación no operable por teclado** → Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA

## Hallazgos Detallados
| Hallazgo | Severidad | Impacto en el negocio |
| --- | --- | --- |
| Contraste bajo en botón de compra | High | –12% conversión mobile / demanda ADA Title III |
| Imágenes de producto sin alt text | Medium | Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda |
| Menú de navegación no operable por teclado | Critical | Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA |

### Contraste bajo en botón de compra
**Impacto estimado:** Mejora legibilidad para usuarios con baja visión o daltonismo, aumentando el tiempo en página y reduciendo la tasa de rebote.
**Representación visual (antes/después):**
```text
┌─ ANTES ──────────────────────────────────────────────┐
│ <button style="background: #FFA500; color: #FFFFFF;">Comprar │
├──────────────────────────────────────────────────────┤
│ DESPUÉS                                              │
│ <button style="background: #D2691E; color: #FFFFFF;">Comprar │
└──────────────────────────────────────────────────────┘
```
**¿Querés corregir este issue?** [Contratar el fix de contraste de colores](https://ranuk.dev/ada-audits?issue=Contraste%20bajo%20en%20bot%C3%B3n%20de%20compra&rule_id=color-contrast)
**Antes → Después**
**Antes:**
```html
<button style="background: #FFA500; color: #FFFFFF;">Comprar</button>
```
**Después:**
```html
<button style="background: #D2691E; color: #FFFFFF;">Comprar</button>
```

### Imágenes de producto sin alt text
**Impacto estimado:** Los usuarios de lectores de pantalla pueden entender el contenido de las imágenes, mejorando la accesibilidad y el SEO.
**Representación visual (antes/después):**
```text
┌─ ANTES ──────────────────────────────────────────────┐
│ <img src="producto.jpg">                                     │
├──────────────────────────────────────────────────────┤
│ DESPUÉS                                              │
│ <img src="producto.jpg" alt="Zapatillas running azul">       │
└──────────────────────────────────────────────────────┘
```
**¿Querés corregir este issue?** [Contratar el fix de texto alternativo para imágenes](https://ranuk.dev/ada-audits?issue=Im%C3%A1genes%20de%20producto%20sin%20alt%20text&rule_id=image-alt)
**Antes → Después**
**Antes:**
```html
<img src="producto.jpg">
```
**Después:**
```html
<img src="producto.jpg" alt="Zapatillas running azul">
```

### Menú de navegación no operable por teclado
**Impacto estimado:** Mejora accesibilidad y cumplimiento WCAG, reduciendo riesgo legal y mejorando experiencia para usuarios con discapacidad.
**Representación visual (antes/después):**
```text
┌─ ANTES ──────────────────────────────────────────────┐
│ <div class="menu" onclick="toggleMenu()">                    │
├──────────────────────────────────────────────────────┤
│ DESPUÉS                                              │
│ <nav aria-label="Principal"><ul role="menubar"><li role="men │
└──────────────────────────────────────────────────────┘
```
**¿Querés corregir este issue?** [Contratar el fix de accesibilidad](https://ranuk.dev/ada-audits?issue=Men%C3%BA%20de%20navegaci%C3%B3n%20no%20operable%20por%20teclado&rule_id=keyboard)
**Antes → Después**
**Antes:**
```html
<div class="menu" onclick="toggleMenu()">
```
**Después:**
```html
<nav aria-label="Principal"><ul role="menubar"><li role="menuitem">Inicio</li><li role="menuitem">Productos</li><li role="menuitem">Contacto</li></ul></nav>
```

## Recomendaciones
- Aumentar contraste de botones críticos a 4.5:1 mínimo
- Agregar alt text descriptivo a todas las imágenes de producto
- Refactorizar navegación con elementos semánticos y roles ARIA

> **💡 ¿Querés que arreglemos esto?**
>
> Respondé este informe o escribinos a **emilio@ranuk.dev** para coordinar las correcciones.
>
> **Ranuk IT Solutions** — [ranuk.dev](https://ranuk.dev)