# Batch 2 — Emails listos 2026-04-17 (tarde)

**Verticales:** Chiropractor Miami + Boutique Hotel Manhattan
**Scan:** 7 sitios, 4 califican como lead. Ordenados por urgencia.

---

## LEAD #4 — Fisher Chiropractic Center 🔴 (Miami — el mejor del batch: 49 elementos + 1 crítico)

**Web:** https://fisherchiropracticcenter.com/
**Para:** `fisherchiropractic@gmail.com` ✅ (email directo encontrado en el sitio)
**Subject:** `quick note about fisherchiropracticcenter.com`

```
Hi there,

Ran an accessibility scan on fisherchiropracticcenter.com this morning and found 49 elements that put it at ADA Title III risk — the same category of issues driving 5,000+ small-practice lawsuits in 2025 (69% against businesses under $25M, and chiropractic/medical are heavily targeted).

Three most urgent:

1. 3 UI elements with color contrast below 4.5:1 (WCAG minimum). This is the #1 trigger for ADA drive-by lawsuits against small practices.

2. One link in your navigation has no discernible text — screen-reader users hit a dead end. Booking flows and contact links are especially exposed.

3. Multiple interactive elements using ARIA attributes incorrectly, breaking screen-reader navigation for blind/low-vision visitors.

I can send you the full 17-point audit (with remediation code your webmaster can copy-paste) — free, no strings. If you want me to fix it, flat $1,200, done in 2 weeks.

Want the report?

— Emilio Ranucoli
Systems Engineer — accessibility & compliance audits
ranuk.dev  |  ranucoliemilio@gmail.com
```

---

## LEAD #5 — Miami Chiropractic (Dr. Wei Huang) 🟠 (26 elementos, 5 imágenes sin alt)

**Web:** https://miamichiropractic.us/
**Para:** `wweeiihhuuaanngg@gmail.com` ✅ (email personal del Dr. Wei Huang)
**Subject:** `quick note about miamichiropractic.us`

```
Hi Wei,

Ran an accessibility scan on miamichiropractic.us this morning and found 26 elements that put it at ADA Title III risk — the same category of issues driving 5,000+ small-practice lawsuits in 2025 (69% against businesses under $25M).

Three most pressing on your site:

1. 5 images without alt text — screen-reader users lose critical context. This is the most-litigated issue category in 2025, especially on medical/chiropractic sites.

2. 5 UI elements with color contrast below 4.5:1. Single most common ADA complaint filed against small practices in FL.

3. An ARIA command control (likely your "book appointment" widget) has no accessible name — blind users can't reach your booking flow.

I can send you the full 17-point report with remediation code — free, no strings. If you want me to execute the fixes, flat $1,200, 2 weeks turnaround.

Want it?

— Emilio Ranucoli
Systems Engineer — accessibility & compliance audits
ranuk.dev  |  ranucoliemilio@gmail.com
```

---

## LEAD #6 — Miami Spine Clinic 🟡 (20 elementos, estructural)

**Web:** https://www.miamispineclinic.com/
**Para:** `info@miamispineclinic.com` (no se encontró email directo, usa este)
**Subject:** `quick note about miamispineclinic.com`

```
Hi there,

Ran a quick accessibility scan on miamispineclinic.com and found 20 structural issues that expose the site to ADA Title III claims — dental, chiropractic and spine clinics are a top target for the 5,000+ small-practice lawsuits filed in 2025.

The three to fix first:

1. The entire page lacks a <main> landmark — screen-reader users can't skip directly to content and hit 19 unlabeled sections.

2. 19 interactive elements (including your "Request Appointment" buttons) sit outside any semantic landmark — blind users can't jump-navigate at all.

3. Missing ARIA labels on your utility navigation — screen readers announce your appointment links without context.

I can send the full audit (17-point report, remediation code included) free. If you want me to fix it, $1,200 flat, 2 weeks.

Want the report?

— Emilio Ranucoli
Systems Engineer — accessibility & compliance audits
ranuk.dev  |  ranucoliemilio@gmail.com
```

---

## LEAD #7 — Library Hotel NYC 🟠 (27 elementos, booking flow comprometido)

**Web:** https://www.libraryhotel.com/
**Para:** `reservations@libraryhotel.com` (estándar para hoteles — si rebota, probar `info@libraryhotel.com`)
**Subject:** `quick note about libraryhotel.com`

```
Hi there,

Ran an accessibility scan on libraryhotel.com this morning and found 27 elements that put it at ADA Title III risk — the same category of issues driving 5,000+ lawsuits in 2025. Hotels are among the top targets, especially NYC properties (NY courts have been the most plaintiff-friendly in the country).

The three most pressing:

1. 6 UI elements with color contrast below 4.5:1, including your address block. This is the #1 trigger for drive-by lawsuits.

2. 7 links with no discernible text — including close-menu and navigation elements. Booking flows are the most legally exposed surface on any hotel site.

3. Non-unique landmarks and missing semantic structure — blind guests can't navigate to your reservation form without trial-and-error.

I can send you the full 17-point audit (with remediation code your webmaster can copy-paste) — free, no strings. If you want me to execute the fixes, flat $1,200, 2 weeks turnaround.

Want the report?

— Emilio Ranucoli
Systems Engineer — accessibility & compliance audits
ranuk.dev  |  ranucoliemilio@gmail.com
```

---

## Pipeline tracking (batch 2)

| Lead | Empresa | Email | Enviado | Respondió | Cerró | $ |
|------|---------|-------|---------|-----------|-------|---|
| #4 | Fisher Chiropractic | fisherchiropractic@gmail.com | | | | |
| #5 | Miami Chiropractic (Wei Huang) | wweeiihhuuaanngg@gmail.com | | | | |
| #6 | Miami Spine Clinic | info@miamispineclinic.com | | | | |
| #7 | Library Hotel NYC | reservations@libraryhotel.com | | | | |

## Comandos para el bot (después de enviar cada uno)

```
ada add-lead https://fisherchiropracticcenter.com/ fisherchiropractic@gmail.com
ada add-lead https://miamichiropractic.us/ wweeiihhuuaanngg@gmail.com
ada add-lead https://www.miamispineclinic.com/ info@miamispineclinic.com
ada add-lead https://www.libraryhotel.com/ reservations@libraryhotel.com
```
