#!/usr/bin/env python3
"""Sistema de outbox para emails listos.

Estructura:
  prospectos/outbox/NN-slug.txt        → emails pendientes de envío
  prospectos/outbox/sent/NN-slug.txt   → ya enviados (se mueven acá al marcar)
  prospectos/outbox/index.json         → metadata de cada email (url, to, subject, sent_date)

Comandos:
  outbox.py list              → lista emails pendientes numerados
  outbox.py show <n>          → muestra email #N listo para copiar
  outbox.py sent <n>          → marca como enviado (mueve a sent/, agrega a leads.csv)
  outbox.py add <url> <email> <firstname> <scan-json>
                              → genera un email nuevo en outbox desde un scan
  outbox.py rebuild           → reescribe todos los outbox files en formato nuevo desde scan-results.json
"""
import json, sys, re, csv, os, shutil
from pathlib import Path
from datetime import date

ROOT = Path("/Users/emilioranucoli/Desktop/ADA-AUDITS")
OUTBOX = ROOT / "prospectos" / "outbox"
SENT = OUTBOX / "sent"
INDEX = OUTBOX / "index.json"
LEADS = ROOT / "prospectos" / "leads.csv"

SENT.mkdir(parents=True, exist_ok=True)


def slugify(domain):
    return re.sub(r'[^a-z0-9]+', '-', domain.lower()).strip('-')[:40]


def load_index():
    if INDEX.exists():
        return json.load(open(INDEX))
    return []


def save_index(data):
    json.dump(data, open(INDEX, "w"), indent=2)


def humanize_issue(issue):
    h = issue.get('help', '').lower()
    n = issue.get('nodes_affected', 0)
    if 'contrast' in h:
        return f"{n} UI elements with color contrast below 4.5:1 (WCAG minimum). This is the #1 trigger for ADA drive-by lawsuits against small practices."
    if 'alternative text' in h or 'alt' in h:
        return f"{n} images without alt text — screen-reader users lose critical context. Most-litigated issue category in 2025."
    if 'discernible text' in h:
        return f"{n} links with no discernible text — screen readers announce them as 'link' with no destination. Booking and contact flows are especially exposed."
    if 'label' in h and 'form' in h:
        return f"{n} form fields without visible labels — blind users hit them and hear only 'edit, blank'."
    if 'landmark' in h and 'main' in h:
        return "The page lacks a main landmark — screen-reader users cannot skip directly to content."
    if 'landmark' in h:
        return f"{n} content blocks sitting outside semantic landmarks — blind users can't jump-navigate."
    if 'color' in h and 'rely' in h:
        return "Links distinguishable only by color — fails WCAG 1.4.1 Use of Color."
    if 'heading' in h:
        return f"{n} headings with hierarchy issues — breaks document outline for assistive tech."
    if 'aria' in h and 'name' in h:
        return f"An interactive control ({n} element) has no accessible name — blind users can't reach the function."
    if 'aria' in h:
        return f"ARIA attributes used incorrectly on {n} element(s), breaking screen-reader navigation."
    return f"{issue.get('help','accessibility issue')} ({n} elements)"


def generate_email_body(domain, first_name, scan_lead):
    """Arma el body del email cold, sin markdown."""
    bullets = [humanize_issue(i) for i in scan_lead.get('top_issues', [])[:3]]
    # Rellenar si hay menos de 3
    while len(bullets) < 3:
        bullets.append("Multiple interactive elements lack proper accessibility metadata, affecting screen-reader users.")

    salutation = f"Hi {first_name}," if first_name and first_name.lower() not in ("there", "") else "Hi there,"
    nodes = scan_lead.get('total_nodes_affected', 0)

    body = f"""{salutation}

Ran an accessibility scan on {domain} this morning and found {nodes} elements that put the site at ADA Title III risk — the same category of issues driving 5,000+ small-business lawsuits in 2025 (69% against companies under $25M).

Three most urgent on your site:

1. {bullets[0]}

2. {bullets[1]}

3. {bullets[2]}

I can send you the full 17-point audit (with remediation code your webmaster can copy-paste) — free, no strings. If you want me to fix it, flat $1,200, done in 2 weeks.

Want the report?

— Emilio Ranucoli
Systems Engineer — accessibility & compliance audits
ranuk.dev  |  ranucoliemilio@gmail.com
"""
    return body


def write_outbox_file(n, meta):
    """Escribe un archivo outbox con el email listo para copy."""
    slug = slugify(meta['domain'])
    filename = f"{n:02d}-{slug}.txt"
    path = OUTBOX / filename

    # Formato: headers arriba (To/Subject) + body en texto plano listo para copiar
    content = f"""EMAIL #{n} — {meta['business_name']}
{'=' * 60}

TO:       {meta['to']}
SUBJECT:  {meta['subject']}

{'─' * 60}
BODY (copy from the line below — do not copy this header)
{'─' * 60}

{meta['body']}
{'─' * 60}
STATUS:   pending
URL:      {meta['url']}
CREATED:  {meta.get('created', date.today().isoformat())}
"""
    path.write_text(content)
    meta['filename'] = filename
    return path


def add(url, to_email, first_name, scan_file):
    """Agrega un email al outbox desde un scan."""
    scans = json.load(open(scan_file))
    lead = next((r for r in scans if r.get('url', '').rstrip('/') == url.rstrip('/')), None)
    if not lead:
        print(f"❌ {url} no está en {scan_file}")
        sys.exit(1)

    domain = re.sub(r'^https?://(www\.)?', '', url).rstrip('/').split('/')[0]
    business_name = " ".join(w.capitalize() for w in domain.split(".")[0].split("-"))

    idx = load_index()
    n = len(idx) + 1
    meta = {
        "n": n,
        "url": url,
        "domain": domain,
        "business_name": business_name,
        "to": to_email,
        "subject": f"quick note about {domain}",
        "first_name": first_name or "there",
        "body": generate_email_body(domain, first_name, lead),
        "status": "pending",
        "created": date.today().isoformat(),
    }
    write_outbox_file(n, meta)
    idx.append(meta)
    save_index(idx)
    print(f"✅ añadido EMAIL #{n} → {meta['filename']}")


def list_cmd():
    idx = load_index()
    pending = [m for m in idx if m.get('status') == 'pending']
    sent = [m for m in idx if m.get('status') == 'sent']

    print(f"📬 Outbox — {len(pending)} pending / {len(sent)} sent\n")
    if pending:
        print("PENDIENTES:")
        for m in pending:
            print(f"  #{m['n']:>2}  {m['business_name'][:30]:30}  → {m['to']}")
        print()
        print(f"Ver email N:       ada email <n>")
        print(f"Marcar enviado:    ada sent <n>")
    else:
        print("✅ Ningún email pendiente.")
    if sent:
        print(f"\nENVIADOS ({len(sent)}):")
        for m in sent[-5:]:
            print(f"  #{m['n']:>2}  {m['business_name'][:30]:30}  {m.get('sent_date','')}")


def show(n):
    idx = load_index()
    m = next((x for x in idx if x['n'] == int(n)), None)
    if not m:
        print(f"❌ no existe email #{n}")
        sys.exit(1)
    # Devolver formato ultra limpio para Telegram copy-paste
    print(f"📧 EMAIL #{m['n']} — {m['business_name']}\n")
    print(f"━━━ TO ━━━")
    print(m['to'])
    print()
    print(f"━━━ SUBJECT ━━━")
    print(m['subject'])
    print()
    print(f"━━━ BODY ━━━")
    print(m['body'].strip())
    print()
    print(f"━━━ DESPUES DE ENVIAR ━━━")
    print(f"ada sent {m['n']}")


def sent_cmd(n):
    idx = load_index()
    m = next((x for x in idx if x['n'] == int(n)), None)
    if not m:
        print(f"❌ no existe email #{n}")
        sys.exit(1)
    if m.get('status') == 'sent':
        print(f"⚠️  email #{n} ya estaba marcado como enviado ({m.get('sent_date')})")
        return

    m['status'] = 'sent'
    m['sent_date'] = date.today().isoformat()

    # Mover archivo a sent/
    fn = m.get('filename')
    if fn:
        src = OUTBOX / fn
        dst = SENT / fn
        if src.exists():
            shutil.move(str(src), str(dst))

    # Agregar a leads.csv
    domain = m['domain']
    # Check si ya existe
    already = False
    if LEADS.exists():
        for r in csv.DictReader(open(LEADS)):
            if r.get('domain', '').replace('www.', '') == domain.replace('www.', ''):
                already = True
                break
    if not already:
        with open(LEADS, 'a') as f:
            # schema: status,domain,business_name,owner_name,owner_email,city,state,industry,scan_score,critical_count,top_issue_1,top_issue_2,top_issue_3,email_sent_date,replied,closed,amount_usd,notes
            row = [
                "pending",
                domain,
                m['business_name'],
                m.get('first_name', ''),
                m['to'],
                "", "", "", "", "",
                "", "", "",
                m['sent_date'],
                "false", "false", "0", ""
            ]
            f.write(",".join(row) + "\n")

    save_index(idx)
    print(f"✅ email #{n} marcado como enviado")
    print(f"   → archivado en outbox/sent/{fn}")
    print(f"   → agregado a leads.csv (email_sent_date={m['sent_date']})")


def rebuild_from_seed():
    """Importa los emails ya creados (batch 1 + batch 2) al nuevo formato."""
    seeds = [
        # Batch 1 - Brooklyn dentists
        ("https://www.brooklynfamilydentalcare.com/", "info@brooklynfamilydentalcare.com", "Terry",
         ROOT / "prospectos" / "scan-results.json", "Brooklyn Family Dental Care"),
        ("https://www.brooklynheightsdental.com/", "info@brooklynheightsdental.com", "there",
         ROOT / "prospectos" / "scan-results.json", "Brooklyn Heights Dental"),
        ("https://www.dentistinbrooklyn.com/", "smile@dentistinbrooklyn.com", "Alex",
         ROOT / "prospectos" / "scan-results.json", "Quentin Smile Dental"),
        # Batch 2 - Chiro Miami + Hotels NYC
        ("https://fisherchiropracticcenter.com/", "fisherchiropractic@gmail.com", "there",
         ROOT / "prospectos" / "batches" / "chiropractor-miami-scan.json", "Fisher Chiropractic Center"),
        ("https://miamichiropractic.us/", "wweeiihhuuaanngg@gmail.com", "Wei",
         ROOT / "prospectos" / "batches" / "chiropractor-miami-scan.json", "Miami Chiropractic"),
        ("https://www.miamispineclinic.com/", "info@miamispineclinic.com", "there",
         ROOT / "prospectos" / "batches" / "chiropractor-miami-scan.json", "Miami Spine Clinic"),
        ("https://www.libraryhotel.com/", "reservations@libraryhotel.com", "there",
         ROOT / "prospectos" / "batches" / "hotel-manhattan-scan.json", "Library Hotel NYC"),
    ]

    # Limpiar
    for f in OUTBOX.glob("*.txt"):
        if f.parent == OUTBOX:
            f.unlink()
    if INDEX.exists():
        INDEX.unlink()

    idx = []
    for i, (url, to, first, scan_file, biz_name) in enumerate(seeds, 1):
        if not Path(scan_file).exists():
            print(f"⚠️  skip {url}: {scan_file} no existe")
            continue
        scans = json.load(open(scan_file))
        lead = next((r for r in scans if r.get('url', '').rstrip('/') == url.rstrip('/')), None)
        if not lead:
            print(f"⚠️  skip {url}: no está en el scan")
            continue
        domain = re.sub(r'^https?://(www\.)?', '', url).rstrip('/').split('/')[0]
        meta = {
            "n": i,
            "url": url,
            "domain": domain,
            "business_name": biz_name,
            "to": to,
            "subject": f"quick note about {domain}",
            "first_name": first,
            "body": generate_email_body(domain, first, lead),
            "status": "pending",
            "created": date.today().isoformat(),
        }
        write_outbox_file(i, meta)
        idx.append(meta)
        print(f"  ✓ #{i:02d} {biz_name}")

    save_index(idx)
    print(f"\n✅ rebuilt: {len(idx)} emails in outbox")


# CLI
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        list_cmd()
    elif cmd == "show":
        show(sys.argv[2])
    elif cmd == "sent":
        sent_cmd(sys.argv[2])
    elif cmd == "add":
        # add <url> <email> <firstname> <scan-json>
        add(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "there",
            sys.argv[5] if len(sys.argv) > 5 else str(ROOT / "prospectos" / "scan-results.json"))
    elif cmd == "rebuild":
        rebuild_from_seed()
    else:
        print(__doc__)
