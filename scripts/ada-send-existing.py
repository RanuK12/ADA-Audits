#!/usr/bin/env python3
import csv, os, sys, json, datetime, subprocess, pathlib

BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))
LEADS_CSV = BASE / 'prospectos' / 'leads.csv'
TEMPLATE_PATH = BASE / 'prospectos' / 'EMAIL-TEMPLATES.md'
OUT_DIR = BASE / 'scripts' / 'tmp'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        txt = f.read()
    # extract Template 1 block
    start = txt.find('## TEMPLATE 1 — Cold opener')
    if start == -1:
        raise RuntimeError('Template 1 not found')
    # find next ##
    end = txt.find('## ', start+1)
    block = txt[start:end].strip()
    # locate the triple backticks
    start_code = block.find('```')
    end_code = block.rfind('```')
    template = block[start_code+3:end_code].strip()
    return template

def fill_template(template, data):
    for key, val in data.items():
        template = template.replace(f'{{{{{key}}}}}', str(val))
    return template

def has_existing_scan(domain):
    """Check if a scan already exists for this domain"""
    folder1 = BASE / 'entregables' / domain.replace('.','_')
    folder2 = BASE / 'entregables' / f"{domain.replace('.','_')}_com"
    
    if folder1.is_dir():
        return folder1 / 'resumen-scan.json', folder1 / 'axe-raw.json'
    elif folder2.is_dir():
        return folder2 / 'resumen-scan.json', folder2 / 'axe-raw.json'
    return None, None

def get_scan_data(domain):
    """Get scan data from existing files only"""
    resumen_path, axe_path = has_existing_scan(domain)
    
    if not resumen_path or not resumen_path.is_file() or not axe_path or not axe_path.is_file():
        return None
        
    with open(resumen_path) as f:
        resumen = json.load(f)
    with open(axe_path) as f:
        axe = json.load(f)
    if isinstance(axe, list):
        axe = axe[0] if axe else {}
    # extract top issues similar to quick-scan output
    violations = axe.get('violations', [])
    order = {'critical':0,'serious':1,'moderate':2,'minor':3}
    top = sorted(violations, key=lambda v: order.get(v.get('impact','minor'),4))[:3]
    top_issues = []
    total_nodes = sum(len(v.get('nodes',[])) for v in violations)
    for v in top:
        issue = v.get('help','')
        top_issues.append(issue)
    return {
        'total_nodes_affected': total_nodes,
        'top_issue_1': top_issues[0] if len(top_issues)>0 else '',
        'top_issue_2': top_issues[1] if len(top_issues)>1 else '',
        'top_issue_3': top_issues[2] if len(top_issues)>2 else '',
    }

def send_email(to, subject, html_body):
    # write html to temp file
    html_path = OUT_DIR / f"email_{to.replace('@','_')}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_body)
    rk_skymailer_script = str(pathlib.Path(os.path.expanduser('~/Apps/ranukita-bridge/scripts/rk-skymailer-send')))
    cmd = ["/bin/bash", rk_skymailer_script, '--to', to,
           '--subject', subject, '--html-file', str(html_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr.strip()
    try:
        out = json.loads(result.stdout.strip())
        status = out.get('status')
        return status == 'sent', out
    except Exception:
        return False, result.stdout.strip()

def main():
    template = load_template()
    today = datetime.date.today().isoformat()
    sent = 0
    failed = 0
    pending = 0
    rows = []
    with open(LEADS_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Only process rows that have actual data (not empty)
            if any(row.get(field) for field in ['domain', 'owner_email', 'business_name']):
                rows.append(row)
    
    print(f"Processing {len(rows)} rows with data...")
    
    for row in rows:
        if row.get('status','').lower() != 'pending':
            continue
        email = row.get('owner_email')
        if not email:
            continue
        domain = row.get('domain')
        if not domain:
            continue
        
        scan = get_scan_data(domain)
        if not scan:
            print(f"No existing scan for {domain}, skipping (will need to generate one)")
            continue
            
        print(f"Processing {domain} with email {email}")
        data = {
            'domain': domain,
            'first_name': row.get('owner_name') or '',
            **scan,
        }
        body = fill_template(template, data)
        subject = f"quick note about {domain}"
        print(f"Sending email to {email} about {domain}")
        ok, info = send_email(email, subject, body)
        if ok:
            row['status'] = 'sent'
            row['email_sent_date'] = today
            sent += 1
            print(f"✅ Sent successfully to {email}")
        else:
            failed += 1
            print(f"❌ Failed to send to {email}: {info}")
    
    # write back CSV
    fieldnames = rows[0].keys() if rows else []
    with open(LEADS_CSV, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    pending = sum(1 for r in rows if r.get('status','').lower()=='pending')
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")
    print(f"Pending: {pending}")
    print(f"Total processed: {len(rows)}")

if __name__ == '__main__':
    main()