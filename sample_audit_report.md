# Auditoría de Accesibilidad WCAG: TiendaOnline Demo
**Fecha:** 2026-09-07
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
**Impacto en el negocio:** –12% conversión mobile / demanda ADA Title III
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
**Impacto en el negocio:** Lectores de pantalla no pueden describir los productos → pérdida de ventas y riesgo de demanda
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
**Impacto en el negocio:** Usuarios sin mouse no pueden navegar → abandono del sitio y posible demanda ADA
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
- Corregir contraste de color en botones y elementos interactivos para cumplir WCAG 2.1 AA (mínimo 4.5:1).
- Agregar texto alternativo descriptivo a todas las imágenes de producto.
- Hacer el menú de navegación operable por teclado usando roles ARIA y gestión de foco.

> **💡 ¿Querés que arreglemos esto?**
>
> Respondé este informe o escribinos a **emilio@ranuk.dev** para coordinar las correcciones.
>
> **Ranuk IT Solutions** — [ranuk.dev](https://ranuk.dev)