#!/usr/bin/env python3
import csv, os, sys, json, subprocess, pathlib, time

BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))
LEADS_CSV = BASE / 'prospectos' / 'leads.csv'
SCAN_SCRIPT = BASE / 'scripts' / 'quick-scan.sh'
OUT_DIR = BASE / 'entregables'

def main():
    # Get all pending leads with no scan
    pending_domains = []
    with open(LEADS_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('status','').lower() != 'pending':
                continue
            domain = row.get('domain')
            if not domain:
                continue
            
            # Check if scan already exists
            folder1 = BASE / 'entregables' / domain.replace('.','_')
            folder2 = BASE / 'entregables' / f"{domain.replace('.','_')}_com"
            
            if folder1.is_dir() or folder2.is_dir():
                print(f"Scan already exists for {domain}, skipping")
                continue
                
            pending_domains.append(domain)
    
    print(f"Found {len(pending_domains)} domains to scan:")
    for d in pending_domains:
        print(f"  - {d}")
    
    # Generate scans one by one
    for i, domain in enumerate(pending_domains):
        url = f"https://{domain}"
        print(f"\n[{i+1}/{len(pending_domains)}] Scanning {url}...")
        
        result = subprocess.run([str(SCAN_SCRIPT), url], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Scan failed for {domain}: {result.stderr}")
            continue
            
        try:
            scan_data = json.loads(result.stdout)
            if scan_data.get('error'):
                print(f"❌ Scan error for {domain}: {scan_data['error']}")
                continue
                
            # Create entregables folder and save scan data
            folder_name = domain.replace('.','_')
            domain_dir = OUT_DIR / folder_name
            domain_dir.mkdir(parents=True, exist_ok=True)
            
            # Save scan result as axe-raw.json
            with open(domain_dir / 'axe-raw.json', 'w') as f:
                json.dump(scan_data, f, indent=2)
            
            # Create resumen-scan.json with summary data
            resumen = {
                'domain': domain,
                'score': scan_data.get('score', 0),
                'critical_count': scan_data.get('critical_count', 0),
                'serious_count': scan_data.get('serious_count', 0),
                'moderate_count': scan_data.get('moderate_count', 0),
                'total_violations': scan_data.get('total_violations', 0),
                'total_nodes_affected': scan_data.get('total_nodes_affected', 0),
                'top_issues': scan_data.get('top_issues', []),
                'qualifies_as_lead': scan_data.get('qualifies_as_lead', False),
                'scan_date': time.strftime('%Y-%m-%d')
            }
            with open(domain_dir / 'resumen-scan.json', 'w') as f:
                json.dump(resumen, f, indent=2)
                
            print(f"✅ Scan generated for {domain} (Score: {scan_data.get('score')}, Critical: {scan_data.get('critical_count')})")
            
        except Exception as e:
            print(f"❌ Error processing scan for {domain}: {str(e)}")

if __name__ == '__main__':
    main()