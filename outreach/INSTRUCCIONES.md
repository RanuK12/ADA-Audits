# Instrucciones: Outreach ADA-AUDITS por Sector

## Qué se creó

1. **5 templates de email sectoriales** en `outreach/templates/`:
   - `ecommerce.json` — Tiendas online, productos, checkout
   - `fintech.json` — Fintech, legal, banca, seguros (compliance)
   - `healthtech.json` — Salud, dental, clínicas, hoteles, restaurantes, fitness
   - `saas.json` — Software, plataformas, startups
   - `gaming.json` — Gaming, esports, entretenimiento

2. **Script de generación**: `outreach/generate_outreach.py`

3. **32 emails pre-generados** en `outreach/emails/` (desde leads.csv actual)

## Cómo usar el script

### Generar emails desde leads.csv (modo rápido)

```bash
cd ~/Desktop/Oficina_Ranuk/ADA-AUDITS/outreach

# Genera 1 email por lead en leads.csv (sin datos de scan)
python3 generate_outreach.py --prospects ../prospectos/leads.csv --quick

# Output: outreach/emails/01-domain.txt, 02-domain.txt, ...
```

### Generar con datos de scan reales

```bash
# Si tenés JSONs de scan en una carpeta:
python3 generate_outreach.py \
  --prospects ../prospectos/leads.csv \
  --scan-dir ../prospectos/scans/

# Los JSONs deben tener: {"total_issues": 25, "issues": ["issue1", "issue2", "issue3"]}
```

### Forzar un sector para todos

```bash
python3 generate_outreach.py \
  --prospects ../prospectos/leads.csv \
  --quick --sector healthtech
```

### Lead manual (uno solo)

```bash
python3 generate_outreach.py --quick \
  --domain "mitienda.com" \
  --business-name "Mi Tienda" \
  --email "info@mitienda.com" \
  --first-name "John" \
  --sector ecommerce
```

### Ver sectores disponibles

```bash
python3 generate_outreach.py --list-sectors
```

### Preview sin generar archivos

```bash
python3 generate_outreach.py --prospects ../prospectos/leads.csv --quick --dry-run
```

## Flujo de envío (paso a paso)

### 1. Generar emails
```bash
cd ~/Desktop/Oficina_Ranuk/ADA-AUDITS/outreach
python3 generate_outreach.py --prospects ../prospectos/leads.csv --quick
```

### 2. Revisar y personalizar (5 min por email)
- Abrir cada archivo en `outreach/emails/`
- Buscar el **nombre real** del dueño/manager en su web o LinkedIn
- Reemplazar "there" por el nombre real en el cuerpo del email
- Si hay datos de scan reales, actualizar los top_issues con los específicos

### 3. Enviar con SkyMailer
```bash
# Para cada email:
~/Apps/ranukita-bridge/scripts/rk-skymailer-send \
  --to "info@ejemplo.com" \
  --subject "asunto del email" \
  --html-file /tmp/body.html

# O manualmente: copiar el body del .txt y pegar en Gmail
```

### 4. Marcar como enviado
- Actualizar `prospectos/leads.csv`: cambiar `email_sent_date` a hoy
- Mover el archivo de `emails/` a `emails/sent/`

## Mapeo de sectores automát

El script detecta el sector automáticamente por nombre de dominio y empresa:

| Palabras clave del dominio/empresa | Sector asignado |
|---|---|
| dental, chiro, medical, spa, fitness, hotel, restaurant, derm | **healthtech** |
| law, legal, injury, attorney, fintech | **fintech** |
| shop, store, commerce, brand | **ecommerce** |
| saas, software, app, platform, tech | **saas** |
| game, gaming, esports | **gaming** |

## Tip de pricing

- **Fase 1 (ahora)**: $800–$1,200 por auditoría completa
- **Pack**: 3 auditorías = $2,400 (ahorra $600)
- **Recurrente**: $200/mes de monitoreo post-fix
- Mínimo absoluto: $800. NUNCA menos.
