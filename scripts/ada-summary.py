#!/usr/bin/env python3
import csv, os, sys, json, datetime, pathlib

BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))
LEADS_CSV = BASE / 'prospectos' / 'leads.csv'

def main():
    sent_count = 0
    pending_count = 0
    total_count = 0
    pending_with_scan = 0
    pending_without_scan = 0
    
    with open(LEADS_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_count += 1
            status = row.get('status', '').lower()
            
            if status == 'sent':
                sent_count += 1
            elif status == 'pending':
                pending_count += 1
                domain = row.get('domain')
                if domain:
                    # Check if scan exists
                    folder1 = BASE / 'entregables' / domain.replace('.','_')
                    folder2 = BASE / 'entregables' / f"{domain.replace('.','_')}_com"
                    if folder1.is_dir() or folder2.is_dir():
                        pending_with_scan += 1
                    else:
                        pending_without_scan += 1
    
    print("=== ADA AUDITS SUMMARY ===")
    print(f"Total leads: {total_count}")
    print(f"Sent: {sent_count}")
    print(f"Pending: {pending_count}")
    print(f"  - With scan available: {pending_with_scan}")
    print(f"  - Without scan: {pending_without_scan}")
    print(f"\nEmails sent today: {sent_count - sum(1 for r in csv.DictReader(open(LEADS_CSV)) if r.get('email_sent_date') == '2026-07-30')}")

if __name__ == '__main__':
    main()