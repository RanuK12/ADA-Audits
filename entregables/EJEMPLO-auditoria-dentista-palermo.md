# Auditoría de Accesibilidad Digital — ADA / WCAG 2.1 AA

**Cliente:** Clínica Dental Sonrisa Palermo (EJEMPLO FICTICIO — USAR COMO MUESTRA)
**Sitio auditado:** https://ejemplo-dental.com.ar
**Fecha:** 2026-04-17
**Auditor:** Emilio Ranúcoli — Consultoría de Accesibilidad Digital
**Normativa de referencia:** ADA Title III + WCAG 2.1 AA

---

## 1. Resumen Ejecutivo

Este reporte documenta **17 hallazgos** de no-conformidad con WCAG 2.1 AA, de los cuales **6 son críticos** con riesgo legal directo bajo ADA Title III. Durante 2025 se registraron más de 5.000 demandas federales por accesibilidad web en EE.UU.; el **69% apuntaron a empresas con facturación menor a USD 25M**. Negocios del rubro salud son blanco prioritario por cruzar además HIPAA + ADA.

- **Nivel de riesgo actual:** ALTO
- **Tiempo estimado de remediación:** 14 horas
- **Costo propuesto:** USD 1.200

### Top 3 riesgos urgentes
1. Formulario de turnos completamente inaccesible por teclado (trampa de focus en selector de fecha).
2. 23 imágenes de tratamientos sin `alt` — incluyendo el CTA principal "Reservar turno".
3. Contraste de 2.1:1 en el botón primario del header (requiere 4.5:1).

---

## 2. Metodología

Auditoría híbrida sobre home, página de servicios, formulario de turnos y landing de promociones. Herramientas: axe-core 4.9, Lighthouse 12, WAVE, revisión semántica asistida por modelo de lenguaje. Flujo transaccional probado: reserva de turno online.

---

## 3. Hallazgos por Severidad

### 🔴 CRÍTICOS

#### C-01 — Imágenes del hero y grilla de servicios sin texto alternativo
- **Criterio WCAG:** 1.1.1 Non-text Content (A)
- **Ubicación:** `index.html` líneas 45–78; componente `<ServicesGrid>`
- **Evidencia:**
  ```html
  <img src="/hero-sonrisa.jpg" class="hero-bg">
  <img src="/servicios/implantes.png">
  ```
- **Impacto:** Usuarios con lector de pantalla (NVDA, VoiceOver, JAWS) escuchan solo "imagen" o el nombre del archivo. El hero promociona una oferta activa — pérdida directa de conversión para 2,3M de argentinos con discapacidad visual.
- **Base legal:** *Robles v. Domino's* (SCOTUS 2019), *Gil v. Winn-Dixie*.
- **Remediación:**
  ```html
  <img src="/hero-sonrisa.jpg" alt="Promo abril: implante dental con corona incluida desde $180.000">
  <img src="/servicios/implantes.png" alt="Implante dental de titanio, procedimiento mínimamente invasivo">
  ```
- **Esfuerzo:** 45 min (23 imágenes)

#### C-02 — Selector de fecha del formulario de turnos no navegable con teclado
- **Criterio WCAG:** 2.1.1 Keyboard (A) + 2.1.2 No Keyboard Trap (A)
- **Ubicación:** `/turnos` — componente `<CustomDatepicker>`
- **Evidencia:** Al llegar con Tab al campo fecha, el foco queda atrapado. Ni Escape ni Tab liberan el widget.
- **Impacto:** Bloqueo total de conversión para usuarios motores que no usan mouse. Es el patrón de demanda *más frecuente* en litigios drive-by.
- **Remediación:** Reemplazar por `<input type="date">` nativo o migrar a `react-datepicker` v7+ que ya implementa WAI-ARIA Authoring Practices. Implementar handlers `onKeyDown` para Escape, flechas y Enter.
- **Esfuerzo:** 2 horas

#### C-03 — Botón "Reservar turno" con contraste 2.1:1
- **Criterio WCAG:** 1.4.3 Contrast (Minimum) (AA)
- **Evidencia:** Texto blanco `#ffffff` sobre rosa pastel `#f4c7d7` → ratio 2.1:1 (mínimo requerido: 4.5:1).
- **Remediación:** Cambiar fondo a `#c73070` → ratio 5.8:1 ✅ (mantiene identidad de marca).
- **Esfuerzo:** 10 min

#### C-04 — Formulario de contacto sin `<label>` asociados
- **Criterio WCAG:** 3.3.2 Labels or Instructions (A) + 4.1.2 Name, Role, Value (A)
- **Evidencia:**
  ```html
  <input type="text" placeholder="Nombre">
  <input type="email" placeholder="Email">
  ```
- **Impacto:** Lectores de pantalla anuncian "campo de edición, vacío" sin contexto. El `placeholder` desaparece al escribir.
- **Remediación:**
  ```html
  <label for="nombre">Nombre completo</label>
  <input id="nombre" type="text" required aria-required="true">
  ```
- **Esfuerzo:** 20 min

#### C-05 — Iframe de Google Maps sin título
- **Criterio WCAG:** 2.4.1 Bypass Blocks + 4.1.2
- **Evidencia:** `<iframe src="https://maps.google.com/..."></iframe>`
- **Remediación:** `<iframe title="Mapa de ubicación de Clínica Dental Sonrisa en Palermo" src="...">`
- **Esfuerzo:** 2 min

#### C-06 — Idioma de página no declarado
- **Criterio WCAG:** 3.1.1 Language of Page (A)
- **Evidencia:** `<html>` sin atributo `lang`.
- **Remediación:** `<html lang="es-AR">`
- **Esfuerzo:** 1 min

---

### 🟠 ALTOS

#### A-01 — Orden de foco ilógico en menú mobile
- **Criterio WCAG:** 2.4.3 Focus Order (A)
- **Evidencia:** Al abrir el burger, el foco va al footer antes que a los ítems del menú.
- **Remediación:** Implementar focus trap + `aria-expanded` en el toggle.
- **Esfuerzo:** 1 h

#### A-02 — Títulos H1 duplicados en home
- **Criterio WCAG:** 1.3.1 Info and Relationships
- **Remediación:** Dejar un único `<h1>`, degradar los demás a `<h2>`.
- **Esfuerzo:** 15 min

#### A-03 — Link "Click acá" sin contexto
- **Criterio WCAG:** 2.4.4 Link Purpose in Context
- **Remediación:** Texto descriptivo: "Reservar turno online" o `aria-label`.
- **Esfuerzo:** 20 min

#### A-04 — Textos con contraste 3.9:1 en footer
- **Criterio WCAG:** 1.4.3
- **Remediación:** Cambiar `#888` a `#5a5a5a`.
- **Esfuerzo:** 5 min

#### A-05 — Errores de formulario solo por color
- **Criterio WCAG:** 1.4.1 Use of Color + 3.3.1
- **Remediación:** Agregar icono + texto + `aria-invalid`.
- **Esfuerzo:** 45 min

---

### 🟡 MEDIOS

- **M-01** Video institucional sin subtítulos (1.2.2) — 2 h
- **M-02** Sin `skip-to-content` link (2.4.1) — 20 min
- **M-03** Tamaño de texto no escalable al 200% (1.4.4) — 30 min
- **M-04** Foco no visible en enlaces del footer (2.4.7) — 15 min

---

### 🔵 BAJOS

- **B-01** Meta description sin traducción alternativa (3.1.2) — 10 min
- **B-02** Favicon no incluye `.svg` accesible — 5 min

---

## 4. Resumen Cuantitativo

| Severidad | Cantidad | Criterios WCAG violados |
|-----------|----------|-------------------------|
| 🔴 Crítico | 6 | 1.1.1, 1.4.3, 2.1.1, 2.1.2, 3.1.1, 3.3.2, 4.1.2 |
| 🟠 Alto    | 5 | 1.3.1, 1.4.1, 1.4.3, 2.4.3, 2.4.4, 3.3.1 |
| 🟡 Medio   | 4 | 1.2.2, 1.4.4, 2.4.1, 2.4.7 |
| 🔵 Bajo    | 2 | 3.1.2, buenas prácticas |
| **Total**  | **17** | |

---

## 5. Plan de Remediación Propuesto

### Fase 1 — Críticos (Semana 1, 5 h)
- Texto alternativo en 23 imágenes
- Reemplazo del datepicker
- Corrección de contraste en CTAs
- Labels + idioma + iframe titles
- **Entrega:** sitio libre de hallazgos rojos + declaración de accesibilidad pública.

### Fase 2 — Altos (Semana 2, 6 h)
- Focus trap de menú mobile
- Jerarquía heading + link purpose
- Errores accesibles en formularios

### Fase 3 — Medios + Bajos (Semana 3, 3 h, opcional)
- Subtítulos en video, skip link, reflow.

**Incluye:** testing manual NVDA + VoiceOver, certificado de cumplimiento WCAG 2.1 AA post-remediación, 30 días de soporte.

**Inversión:** **USD 1.200** — 50% inicio (USD 600) / 50% entrega.

---

## 6. Qué ocurre si no se remedia

- **Demandas drive-by:** USD 10–75k por arreglo extrajudicial.
- **Pérdida de mercado:** 1 de cada 4 argentinos tiene alguna discapacidad (INDEC 2022). Sitio inaccesible = exclusión de ingresos.
- **SEO:** Google Core Web Vitals penaliza mala semántica.

---

## 7. Anexos

- A1. Reporte axe-core completo (`axe-report.json`)
- A2. 14 capturas con hallazgos señalados
- A3. Declaración de accesibilidad modelo
- A4. Checklist WCAG 2.1 AA (50 criterios, estado actual)

---

**Ejecutar remediación:**
Emilio Ranúcoli
ranucoliemilio@gmail.com
[Calendly]

*Confidencial. No constituye asesoramiento legal.*
