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
import csv
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

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
    n = issue.get('nodes_affected', 0) or 1
    el = f"{n} element" if n == 1 else f"{n} elements"
    if 'contrast' in h:
        return f"Color contrast on {el} falls below the 4.5:1 threshold, making text and buttons harder to read on mobile screens or in bright light (WCAG 1.4.3)."
    if 'alternative text' in h or 'alt' in h:
        return f"{n} {'images are' if n>1 else 'image is'} missing descriptive 'alt' attributes in the HTML, which hurts Google image indexing and leaves screen-reader users without context (WCAG 1.1.1)."
    if 'discernible text' in h:
        return f"{n} interactive {'buttons or links lack' if n>1 else 'button or link lacks'} a clear text label in the code, so assistive browsers can't tell visitors where they lead (WCAG 4.1.2)."
    if 'label' in h and 'form' in h:
        return f"{n} form {'fields lack' if n>1 else 'field lacks'} explicit code labels, which can cause mobile autofill and keyboard navigation to fail on contact/booking forms (WCAG 3.3.2)."
    if 'landmark' in h and 'main' in h:
        return "The page layout is missing a primary <main> semantic landmark, making keyboard and assistive navigation slower."
    if 'landmark' in h:
        return f"{el} {'sit' if n>1 else 'sits'} outside semantic HTML landmark regions, which makes it harder for assistive tech to jump-navigate the page."
    if 'color' in h and 'rely' in h:
        return "Links are distinguishable only by color, making them harder to spot for low-vision visitors (WCAG 1.4.1)."
    if 'heading' in h:
        return f"{n} {'headings skip' if n>1 else 'heading skips'} hierarchy levels (e.g., jumping from H2 to H4), which confuses both search engine crawlers and screen readers."
    if 'aria' in h and 'name' in h:
        return f"An interactive control ({el}) has no accessible name in the code, preventing assistive navigation."
    if 'aria' in h:
        return f"{el} {'have' if n>1 else 'has'} mismatched ARIA attributes in the DOM, which can cause focus traps when navigating on mobile or by keyboard."
    return f"{issue.get('help','Technical accessibility barrier')} ({el} affected in the DOM)."


def generate_email_body(domain, first_name, scan_lead):
    """Arma el body del email cold con el formato humanizado de Ranuk IT Solutions."""
    bullets = [humanize_issue(i) for i in scan_lead.get('top_issues', [])[:3]]
    while len(bullets) < 3:
        bullets.append("Several interactive controls are missing explicit ARIA labels in the HTML, making keyboard navigation harder (WCAG 4.1.2).")

    is_person = bool(first_name and first_name.lower() not in ("there", "info", "contact", "admin", "team", "office", ""))
    salutation = f"Hi {first_name}, hope your week is going well." if is_person else "Hi everyone, hope you're having a great week."
    nodes = scan_lead.get('total_nodes_affected', 0)
    dev_target = "your web developer" if is_person else "your web developer or team"

    body = f"""{salutation}

My name is Emilio Ranucoli, and I run Ranuk IT Solutions (ranuk.dev), a software engineering and technical auditing firm. To be completely transparent with you: instead of sending generic sales pitches, the way we introduce our work and earn new clients is by proactively reviewing websites of businesses we come across, spotting technical errors that often go unnoticed, and sharing what we found upfront.

I spent some time analyzing {domain} earlier today and noticed a few specific code issues (across {nodes} elements) that are currently affecting mobile usability, search visibility, and WCAG / ADA accessibility:

1. {bullets[0]}

2. {bullets[1]}

3. {bullets[2]}

Aside from keeping the site aligned with current ADA Title III / WCAG 2.1 AA standards, fixing these small friction points makes it much easier for mobile visitors to navigate and reach out without getting stuck.

If you'd like to see who we are, our engineering standards, and some of the live web platforms and software projects we build, feel free to take a look at our portfolio at ranuk.dev/portfolio (or our main site at ranuk.dev).

I already put together a clean technical report showing where these issues are and the exact code snippets {dev_target} would need to fix them (or if you ever need an extra pair of hands, our team can also handle the fixes for you).

There's no catch or cost—it's simply how we introduce ourselves. Mind if I send the PDF report your way so you have it on hand?

Best regards,

Emilio Ranucoli
Systems Engineer · Founder, Ranuk IT Solutions
Portfolio: ranuk.dev/portfolio  |  ranuk.dev
emilio@ranuk.dev
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
        print("Ver email N:       ada email <n>")
        print("Marcar enviado:    ada sent <n>")
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
    print("━━━ TO ━━━")
    print(m['to'])
    print()
    print("━━━ SUBJECT ━━━")
    print(m['subject'])
    print()
    print("━━━ BODY ━━━")
    print(m['body'].strip())
    print()
    print("━━━ DESPUES DE ENVIAR ━━━")
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
