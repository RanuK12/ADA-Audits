# Criterios de Targeting — ADA Audits & Outbound Ranuk IT Solutions

## Verticals Prioritarias (Perfil B2B Validado — Caso Ramón Borrás)

Validado en producción: los mejores clientes con mayor tasa de respuesta, presupuesto y necesidad de servicios de software/IA/accesibilidad son agencias digitales, estudios de diseño, empresas de tecnología y consultoras de servicios profesionales.

### Tier 1: Prioridad Máxima (Agencias, Tech, Diseño y Consultoría)
- **Agencias de publicidad y comunicación (`office=advertising_agency`, `office=marketing`)**
  - Motivo: Tienen clientes corporativos, sufren de webs lentas en WordPress, buscan activamente modernización a Jamstack/Astro y automatización de leads con agentes de IA. (Perfil validado: Ramón Borrás).
  - Ticket: 390 € - 1.500 € (auditoría, migración web a Astro, bot RAG de atención).
  - Contacto: Fundador, Director de Tecnología, contacto@, hola@.

- **Empresas de tecnología y software (`office=it`)**
  - Motivo: Alto conocimiento técnico, exigencia de cumplimiento normativo (EAA / WCAG 2.1 AA) y contratación de desarrollo por capacidad.
  - Ticket: 500 € - 2.500 €.

- **Estudios de diseño web y branding (`office=web_design`, `office=graphic_design`)**
  - Motivo: Necesitan garantizar que los sitios entregados a sus clientes cumplan accesibilidad y no tengan sobrecarga técnica ni bloat de plugins.
  - Ticket: 390 € - 1.200 €.

- **Consultoras estratégicas y de gestión (`office=consulting`)**
  - Motivo: Portales corporativos B2B que requieren máxima velocidad de carga, intake de leads automatizado y reputación institucional.
  - Ticket: 590 € - 1.800 €.

### Tier 2: Servicios Profesionales de Alto Ticket
- **Estudios de arquitectura (`office=architect`)**
  - Motivo: Portfolios visuales pesados que colapsan en móviles; alto presupuesto de branding y presencia digital.
  - Ticket: 490 € - 1.500 €.

- **Firmas legales y bufetes (`office=lawyer`)**
  - Motivo: Alto riesgo regulatorio ADA / EAA, formularios de contacto complejos sin accesibilidad, alto ticket medio.
  - Ticket: 800 € - 2.000 €.

- **Asesorías fiscales y contables (`office=accountant`, `office=financial`)**
  - Motivo: Portales de clientes, cumplimiento técnico normativo y necesidad de automatización documental.
  - Ticket: 400 € - 1.200 €.

- **Inmobiliarias boutique (`office=estate_agent`)**
  - Motivo: Buscadores de inmuebles lentos en móviles, necesidad de asistentes virtuales de atención rápida 24/7.
  - Ticket: 500 € - 1.500 €.

---

## Criterios de Filtrado y Scoring de Leads

### ✅ Señales de Alta Conversión (Fit Score $\ge 75$):
- Rubro agencia / consultoría / tecnología (+15 pts).
- Sitio desarrollado en **WordPress** (`wp-content`, `wp-includes`): candidato perfecto para ofrecer migración a Astro / Jamstack ultrarrápido y seguro (+15 pts).
- **Sin bot conversacional ni WhatsApp** visible: candidato directo para integración de agente de IA (+15 pts).
- No adaptado a móvil / sin viewport (+15 pts).
- Sin HTTPS o certificado desactualizado (+10 pts).
- Copyright desactualizado ($\le 2024$) (+10 pts).

### ❌ Exclusión Estricta (Comercios y servicios B2C locales):
- Comercios minoristas: peluquerías, talleres mecánicos, cerrajerías, ópticas, farmacias, veterinarias, autoescuelas.
- Sitios sin dominio propio (subdominios wix/linktree/facebook).
- Dominios sin MX o que no resuelven correo.
