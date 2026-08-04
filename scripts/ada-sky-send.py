#!/usr/bin/env python3
"""Envío de emails pendientes del outbox usando SkyMailer.

Requiere: SkyMailer instalado (~/Desktop/Oficina_Ranuk/SkyMailer) y script
rk-skymailer-send disponible.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path('/Users/emilioranucoli/Desktop/Oficina_Ranuk/ADA-AUDITS')
OUTBOX = ROOT / 'prospectos' / 'outbox'
INDEX = OUTBOX / 'index.json'
SENT_DIR = OUTBOX / 'sent'

def load_index():
    if INDEX.exists():
        return json.load(open(INDEX))
    return []

def save_index(data):
    json.dump(data, open(INDEX, 'w'), indent=2)

def send_email(entry):
    # Prepare HTML body
    html_path = Path('/tmp/ada_email_body.html')
    html_content = f"<html><body>{entry['body'].replace('\n','<br>')}</body></html>"
    html_path.write_text(html_content)
    # Build command
    cmd = [
        str(Path.home() / 'Apps' / 'ranukita-bridge' / 'scripts' / 'rk-skymailer-send'),
        '--to', entry['to'],
        '--subject', entry['subject'],
        '--html-file', str(html_path)
    ]
    # If PDF exists for this domain, attach it
    pdf_path = ROOT / 'output' / f"ADA_Audit_{entry['domain'].replace('.','_')}.pdf"
    if pdf_path.exists():
        cmd.extend(['--attach', str(pdf_path)])
    # Run
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ error sending to {entry['to']}: {result.stderr.strip()}", file=sys.stderr)
        return False
    # Expect JSON output like {"to":"...","status":"sent"}
    try:
        resp = json.loads(result.stdout.strip())
        if resp.get('status') != 'sent':
            print(f"⚠️ SkyMailer returned not sent: {resp}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"⚠️ cannot parse SkyMailer output: {e}", file=sys.stderr)
        return False
    return True

def main():
    index = load_index()
    pending = [e for e in index if e.get('status') == 'pending']
    if not pending:
        print('✅ no hay emails pendientes')
        return
    sent_cnt = 0
    for entry in pending:
        if send_email(entry):
            # mark sent
            entry['status'] = 'sent'
            entry['sent_date'] = datetime.now().isoformat()
            # move txt file
            src = OUTBOX / entry['filename']
            dst = SENT_DIR / entry['filename']
            if src.exists():
                src.rename(dst)
            sent_cnt += 1
    save_index(index)
    print(f'✅ enviados: {sent_cnt}')

if __name__ == '__main__':
    main()
