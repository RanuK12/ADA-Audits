# ADA Audits — Sistema de Monetización Fase 1

**Objetivo:** recuperar Mac + costo Claude en 2–3 semanas cerrando 1 cliente/semana a USD 800–1.200.

## Estructura

```
ADA-AUDITS/
├── README.md                       ← este archivo
├── FLUJO-DIARIO.md                 ← rutina de 2h/día. Leer primero.
├── templates/
│   ├── PLANTILLA-AUDITORIA.md      ← formato del entregable final
│   └── PROMPT-GENERAR-AUDITORIA.md ← prompt maestro para Claude
├── scripts/
│   ├── fetch-site.sh               ← descarga HTML + axe + lighthouse
│   └── quick-scan.sh               ← escaneo 30s → decide si es lead
├── prospectos/
│   ├── CRITERIOS-TARGETING.md      ← quién es ICP, quién no
│   ├── EMAIL-TEMPLATES.md          ← 5 plantillas cold + follow-up + objeciones
│   └── leads.csv                   ← pipeline
└── entregables/
    └── EJEMPLO-auditoria-dentista-palermo.md  ← muestra terminada
```

## Primer día (hoy, 90 min)

1. Leer `FLUJO-DIARIO.md` completo (10 min).
2. Leer `prospectos/CRITERIOS-TARGETING.md` y `EMAIL-TEMPLATES.md` (15 min).
3. Instalar herramientas:
   ```bash
   npm i -g @axe-core/cli puppeteer lighthouse
   ```
4. Elegir 1 vertical + 1 ciudad US del target list. Ej: `dentistas Brooklyn NY`.
5. Buscar en Google Maps, copiar 10 URLs a `prospectos/urls-del-dia.txt`.
6. Correr `./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt`.
7. Mandar 5 emails personalizados con Template 1.

## Reglas que no se negocian

- Precio mínimo USD 800. Nunca menos.
- 50% upfront siempre.
- Sitios solo US (ADA no aplica afuera).
- Evidencia específica en el primer email — genérico = 0% respuesta.
- No automatizar envío de emails en Fase 1. Personalizado 1-a-1.

## Siguiente fase

Mientras este sistema genera cash, Gumroad/Twitter/Reddit corren en background (Fase 2 pasiva). Después del 3er cliente cerrado, arrancar Fase 3 (Micro-SaaS) en paralelo.
