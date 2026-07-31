#!/usr/bin/env python3
import csv, os, sys, json, datetime, subprocess, pathlib

BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))
LEADS_CSV = BASE / 'prospectos' / 'leads.csv'

def main():
    # Load data
    with open(LEADS_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            if any(row.get(field) for field in ['domain', 'owner_email', 'business_name']):
                rows.append(row)
    
    # Summary statistics
    total_leads = len(rows)
    sent_leads = len([r for r in rows if r.get('status','').lower() == 'sent'])
    pending_leads = len([r for r in rows if r.get('status','').lower() == 'pending'])
    
    # Get domain statistics
    domains = [r['domain'].split('.')[-1] for r in rows if r.get('domain')]
    domain_counts = {}
    for d in domains:
        domain_counts[d] = domain_counts.get(d, 0) + 1
    
    # Email domain statistics
    email_domains = [r['owner_email'].split('@')[-1] for r in rows if r.get('owner_email')]
    email_counts = {}
    for e in email_domains:
        email_counts[e] = email_counts.get(e, 0) + 1
    
    # Create report
    report = f"""ADA AUDIT OUTREACH SUMMARY REPORT
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== OVERALL STATISTICS ===
Total Leads with Data: {total_leads}
Successfully Sent: {sent_leads}
Pending: {pending_leads}
Success Rate: {sent_leads/total_leads*100:.1f}%

=== DOMAIN DISTRIBUTION (Top 20) ===
"""
    
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        report += f"{domain}: {count}\n"
    
    report += "\n=== EMAIL DOMAIN DISTRIBUTION (Top 20) ===\n"
    for email, count in sorted(email_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        report += f"{email}: {count}\n"
    
    report += "\n=== RECENT SENT EMAILS ===\n"
    recent_sent = [r for r in rows if r.get('status','').lower() == 'sent']
    recent_sent.sort(key=lambda r: r.get('email_sent_date', ''), reverse=True)
    for row in recent_sent[:20]:
        report += f"- {row['domain']} ({row['owner_email']}) on {row.get('email_sent_date', 'N/A')}\n"
    
    # Save report
    report_path = BASE / 'prospectos' / 'outreach-summary-report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report saved to: {report_path}")
    print("\n=== REPORT SUMMARY ===")
    print(f"Total Leads: {total_leads}")
    print(f"Successfully Sent: {sent_leads}")
    print(f"Pending: {pending_leads}")
    print(f"Success Rate: {sent_leads/total_leads*100:.1f}%")
    print(f"\nFull report saved to: {report_path}")

if __name__ == '__main__':
    main()