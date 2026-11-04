#!/usr/bin/env python3
"""Genera un email cold personalizado a partir del scan results.

Uso: generate-pitch.py <url> <scan-results.json>
Imprime el email en stdout listo para copiar.
"""
import json
import re
import sys
from pathlib import Path

url, scan_file = sys.argv[1], sys.argv[2]
scans = json.load(open(scan_file))
lead = next((r for r in scans if r.get('url') == url or r.get('url','').rstrip('/') == url.rstrip('/')), None)
if not lead:
    print(f"❌ URL no encontrada en {scan_file}. Corré primero: ada scan <url>")
    sys.exit(1)
if lead.get('error'):
    print(f"❌ este scan falló: {lead['error']}")
    sys.exit(1)

domain = re.sub(r'^https?://(www\.)?', '', url).rstrip('/').split('/')[0]

# Traducir issues técnicos a lenguaje de venta
def humanize(issue):
    h = issue.get('help','').lower()
    impact = issue.get('impact','')
    n = issue.get('nodes_affected', 0)
    sample = issue.get('sample_html','')[:150]

    if 'contrast' in h:
        return f"{n} UI elements with color contrast below WCAG minimum (4.5:1). This is the #1 trigger for ADA drive-by lawsuits against small practices."
    if 'alternative text' in h or 'alt' in h:
        return f"{n} image(s) without alt text — screen-reader users lose critical context. Most-litigated issue category in 2025."
    if 'discernible text' in h:
        return f"{n} link(s) with no discernible text — screen readers announce them as 'link' with no destination. Booking/contact flows are especially exposed."
    if 'label' in h and 'form' in h:
        return f"{n} form field(s) without visible labels — blind users hit them and hear only 'edit, blank'."
    if 'landmark' in h:
        return f"{n}+ content block(s) sitting outside semantic landmarks. Screen-reader users can't jump-navigate the page."
    if 'color' in h and 'rely' in h:
        return "Links distinguishable only by color — fails WCAG 1.4.1 Use of Color."
    if 'lang' in h:
        return "Missing language attribute on <html> — screen readers mispronounce content."
    if 'heading' in h or 'h1' in h:
        return f"{n} heading(s) with hierarchy issues — breaks document outline for assistive tech."
    # fallback genérico
    return f"{issue.get('help','accessibility issue')} ({n} element{'s' if n!=1 else ''})"

bullets = []
for issue in lead.get('top_issues', [])[:3]:
    bullets.append(humanize(issue))

# Construir pitch
score_color = "🔴" if lead['critical_count']>0 else ("🟠" if lead['serious_count']>2 else "🟡")

email = f"""Subject: a few technical notes I put together for {domain}

Hi {{{{first_name}}}}, hope your week is going well.

My name is Emilio Ranucoli, and I run Ranuk IT Solutions (ranuk.dev), a software engineering and technical auditing firm. To be completely transparent with you: instead of sending generic sales pitches, the way we introduce our work and earn new clients is by proactively reviewing websites of businesses we come across, spotting technical errors that often go unnoticed, and sharing what we found upfront.

I spent some time analyzing {domain} earlier today and noticed a few specific code issues (across {lead['total_nodes_affected']} elements) that are currently affecting mobile usability, search visibility, and WCAG / ADA accessibility:

1. {bullets[0] if len(bullets)>0 else '(no top issue)'}

2. {bullets[1] if len(bullets)>1 else '(no 2nd issue)'}

3. {bullets[2] if len(bullets)>2 else '(no 3rd issue)'}

Aside from keeping the site aligned with current ADA Title III / WCAG 2.1 AA standards, fixing these small friction points makes it much easier for mobile visitors to navigate and contact you without getting stuck.

I already put together a clean technical report showing where these issues are and the exact code snippets your web developer would need to fix them (or if you ever need an extra pair of hands, our team can also handle the fixes for you).

There's no catch or cost—it's simply how we introduce ourselves. Mind if I send the PDF report your way so you have it on hand?

Best regards,

Emilio Ranucoli
Systems Engineer · Founder, Ranuk IT Solutions
ranuk.dev  |  emilio@ranuk.dev"""

print("=" * 60)
print(f"{score_color} LEAD: {domain}")
print(f"  score={lead['score']}  crit={lead['critical_count']}  serious={lead['serious_count']}  nodes={lead['total_nodes_affected']}")
print("=" * 60)
print()
print(email)
print()
print("=" * 60)
print("ANTES DE ENVIAR:")
print("  1. Buscar nombre del owner en la About page + LinkedIn (2 min)")
print("  2. Conseguir email en hunter.io o apollo.io (1 min)")
print("  3. Reemplazar {{first_name}}")
print("  4. ada add-lead", url, "<email>")
print("=" * 60)

# Guardar también a archivo
out_dir = Path("/Users/emilioranucoli/Desktop/ADA-AUDITS/prospectos/pitches")
out_dir.mkdir(exist_ok=True)
out_file = out_dir / f"{domain.replace('.','_')}.txt"
out_file.write_text(email)
print(f"\n💾 guardado en: {out_file}")
