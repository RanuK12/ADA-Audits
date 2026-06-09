# STRATEGY-US.md — ADA Audits Outreach Playbook (USA)

> Última actualización: 2026-06-06 (Saturday)
> Account: emilio@ranuk.dev
> Template: EMAIL-TEMPLATE-PRO.html (HTML profesional con logo + CTA)

## Resumen ejecutivo
- **Servicio**: Auditoría de accesibilidad web ADA/WCAG 2.1 AA
- **Mercado**: PyMAs USA con presencia web (dental, legal, med spa, chiropractic, hotel, restaurant, fitness)
- **Precio**: Auditoría GRATIS + fix flat $1,200 (2 semanas, garantía compliance)
- **Propuesta de valor**: Reducir exposición a demandas ADA (5,000+/año, $15k-$35k settlement promedio)

## Ángulos probados y performance (80 emails, Jun 2-5)

| Variante | Subject example | % usada | Notas |
|----------|-----------------|---------|-------|
| **B (risk-first)** | `{domain} has ada compliance gaps` | 40% | **GANADORA** — más consistente. Mentionar dominio + gaps concretos |
| **C (social proof)** | `audit results for {domain}` | 30% | Segunda mejor. Curiosidad implícita |
| **D (deadline Q3)** | `needs wcag fixes before q3` | 15% | Decente pero declinante. Q3 peak lawsuits |
| **E (revenue risk)** | `{domain} is losing visitors` | 15% | Nueva. Testear más. Ángulo SEO/revenue vs legal |
| **A (baseline)** | `quick note about {domain}` | 0% | **ELIMINADA** — no aporta diferencial |

### 🎯 Hipótesis del día (2026-06-06)
**"B sigue siendo la más fuerte (40%). Para hoy: B=50%, C=25%, E=25%. NO mandar D ni A. EXPANSIÓN GEO: estados nuevos (IL, OH, MI, TN, NV, AZ, SC, LA). Sectores nuevos: veterinary, accounting, automotive repair. Timing ideal: 8-10am hora del prospecto. Espaciar envíos: máximo 4 cada 15 min para evitar spam filter."**

### Razonamiento:
1. B domina desde Jun 2 (55%→30%→35%→40%) → escalarla a 50%
2. C es sólida segunda → mantener 25%
3. E es nueva, solo 2 días de data → subir a 25% para tener más muestras
4. D declinó (30%→20%→15%) → pausar, revisar en 72h
5. A eliminada definitivamente
6. 80 emails, 0 replies → normal para cold outreach. El reply rate industry es 1-3%. Esperar Jun 2-4 results.

## Sectores priorizados (por potencial ADA)

| Sector | Prioridad | Por qué |
|--------|-----------|---------|
| Dental practices | ⭐⭐⭐ | Alta demanda ADA, website critical, decision maker fácil de encontrar |
| Law firms | ⭐⭐⭐ | Conocen riesgo legal, Higher ticket potential |
| Med spas | ⭐⭐ | Website-heavy, buen revenue, target audience young |
| Chiropractic | ⭐⭐ | Similar a dental, websites a menudo mal hechos |
| Hotels/boutique | ⭐⭐ | High traffic, booking funnel = ADA critical |
| Restaurants | ⭐ | Menos budget pero websites suelen tener muchos issues |
| Veterinary | ⭐ | NUEVO — testear. Similar profile a dental |
| Accounting | ⭐ | NUEVO — websites estáticos, buen fit para fixes rápidos |

## Estados cubiertos (Jun 2-5)
FL, NY, CA, PA, TX, CO, GA, NC, VA, WA, OR, MA, MD, WI

## Estados NUEVOS para hoy
IL, OH, MI, TN, NV, AZ, SC, LA

## Template email
- Archivo: `prospectos/EMAIL-TEMPLATE-PRO.html`
- Variables: `{{first_name}}`, `{{business_name}}`, `{{domain}}`, `{{issue_1..3}}`
- Subject: variante B/C/E según distribución del día
- Logo: `ranuk-it-logo.png` via Content-ID `ranuklogo`
- Envío: `rk-skymailer-send --html-file ... --inline ranuklogo=...`

## Reglas de envío
1. Máximo 20 emails/día
2. Espaciar: 4 emails cada 15 min
3. Empezar por costa EST (8-10am ET), avanzar hacia west
4. Nunca mandar los 20 de golpe
5. SIEMPRE verificar status:sent antes de contar
6. Email genérico (info@/contact@) → enviar igual

## Métricas acumuladas
- Semana 1 (Jun 2-6): 80 enviados, 0 replies (esperando 72h)
- Reply rate target: 2-5% (1-4 replies de los primeros 80)
- Revenue target: 1 cliente = $800-$1,200

## Mejoras diarias
1. Revisar replies de 72h atrás cada mañana
2. Doblar variant ganadora, matar la perdedora
3. Expandir geografía (no repetir estado más de 6x/semana)
4. Variedad de sectores (no más de 40% en un solo sector)
5. Personalizar nombre del owner (LinkedIn/About page) cuando sea posible
