# Plantillas de Email Frío — ADA Audits

**Reglas inviolables:**
- Subject line máx 6 palabras, minúscula, sin clickbait.
- Primer email ≤ 80 palabras. Nunca mandes el reporte entero: mandás 3 hallazgos concretos con screenshot/código.
- Usar el nombre del dueño, no "Hi team". LinkedIn + About page del sitio dan el nombre en 30 segundos.
- Incluir evidencia específica del sitio del prospecto, no genérica. Esto es lo que separa 2% de respuesta vs 15%.
- Nunca mencionar "demanda" en el subject. En el body sí, una vez.

---

## TEMPLATE 1 — Cold opener (inglés, para clientes US)

**Subject:** `quick note about {{domain}}`

```
Hi {{first_name}},

Ran a quick accessibility scan on {{domain}} this morning and found 3 issues that put the site at risk under ADA Title III — the same category of issues driving 5,000+ small-business lawsuits in 2025 (69% against companies under $25M).

The three most urgent on your site:
1. {{issue_1_with_location}}
2. {{issue_2_with_location}}
3. {{issue_3_with_location}}

I can send you the full audit (17-point report with remediation code) — free, no strings. If you want me to fix it, I charge a flat $1,200 and it's done in 2 weeks.

Want the report?

— Emilio
```

### Variables a rellenar ANTES de enviar
- `{{first_name}}`: nombre del owner/marketing lead.
- `{{domain}}`: sin https://
- `{{issue_N_with_location}}`: ejemplos reales:
  - *"The 'Book Appointment' button has 2.1:1 contrast — fails WCAG and is the #1 drive-by lawsuit trigger"*
  - *"23 product images on /shop have no alt text"*
  - *"The date picker in the contact form traps keyboard users"*

---

## TEMPLATE 2 — Follow-up 1 (día +3, si no respondieron)

**Subject:** `re: {{domain}}`

```
{{first_name}}, bumping this up. Attached a 2-page preview of the audit.

If the full report is useful, just reply "send it" and I'll forward. Fixing the top 3 criticals takes ~4 hours and removes the immediate litigation exposure.

Fair to ping you once more next week, or should I close the loop?

— Emilio
```

---

## TEMPLATE 3 — Follow-up 2 (día +7, último)

**Subject:** `closing the loop on {{domain}}`

```
{{first_name}} — not going to keep emailing. If accessibility isn't on the radar this quarter, totally fair.

One thing worth knowing: the two law firms running most ADA drive-by suits in {{state}} specifically look for the contrast/keyboard/alt-text combo your site currently has. Average settlement is $15k-$35k.

If that changes your priorities, I'm here. Otherwise, good luck with the rest of the year.

— Emilio
```

---

## TEMPLATE 4 — Llegó respuesta "send it"

**Subject:** `{{domain}} — full audit attached`

```
{{first_name}}, here's the full report.

17 findings, prioritized by legal exposure, each with remediation code you or your dev can copy-paste. If you want me to execute the fixes, scope is:

  • Phase 1 (criticals, week 1) — $800
  • Phase 1 + 2 (criticals + high, weeks 1-2) — $1,200  ← recommended
  • Full remediation + compliance statement + 30-day support — $1,800

I take 50% upfront. Can start {{next_week_monday}}. Calendly: {{link}}

— Emilio
```

---

## TEMPLATE 5 — Respuesta objeción "we're not US / too expensive / we have a widget"

### Objeción: "We have AccessiBe / UserWay"
```
Widgets overlay on top of the site — they don't fix the underlying code. The 2024 *Murphy v. Harris Jewelry* ruling specifically found that overlays don't satisfy ADA. You'd still lose the case. Want to see which of your issues the widget is actually missing?
```

### Objeción: "Too expensive"
```
Understood. For context: typical drive-by settlement is $15-35k plus your lawyer's time. The $1,200 is the *cheap* insurance. If it's a cash-flow issue, I do 3 monthly payments of $450 — happy to send that as an option.
```

### Objeción: "We're not US-based / no US customers"
```
Got it, you're probably out of scope then. ADA only applies if you have US visitors or sell to US. One check: open Google Analytics → Audience → Geo. If >5% US traffic, you're technically liable. If not, you're clear and I won't bother you.
```
