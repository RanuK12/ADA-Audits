#!/usr/bin/env python3
import csv, os, sys, json, datetime, subprocess, pathlib

try:
    import pandas as pd
except ImportError:
    pd = None

BASE = pathlib.Path(os.path.expanduser('~/Desktop/Oficina_Ranuk/ADA-Audits'))
LEADS_CSV = BASE / 'prospectos' / 'leads.csv'

def main():
    # Load data
    if pd:
        df = pd.read_csv(LEADS_CSV)
        
        # Filter rows with actual data
        df_valid = df[df[['domain', 'owner_email', 'business_name']].notna().any(axis=1)]
        
        # Summary statistics
        total_leads = len(df_valid)
        sent_leads = len(df_valid[df_valid['status'].str.lower() == 'sent'])
        pending_leads = len(df_valid[df_valid['status'].str.lower() == 'pending'])
        
        # Get domain statistics
        domain_stats = df_valid['domain'].str.split('.').str[-1].value_counts()
        
        # Get email domain statistics
        email_domains = df_valid['owner_email'].str.split('@').str[-1].value_counts()
        
        # Create report
        report = f"""ADA AUDIT OUTREACH SUMMARY REPORT
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== OVERALL STATISTICS ===
Total Leads with Data: {total_leads}
Successfully Sent: {sent_leads}
Pending: {pending_leads}
Success Rate: {sent_leads/total_leads*100:.1f}%

=== DOMAIN DISTRIBUTION ===
{domain_stats.to_string()}

=== EMAIL DOMAIN DISTRIBUTION ===
{email_domains.head(10).to_string()}

=== RECENT SENT EMAILS ===
"""
        
        # Get recently sent emails
        recent_sent = df_valid[df_valid['status'].str.lower() == 'sent'].sort_values('email_sent_date', ascending=False)
        if 'email_sent_date' in recent_sent.columns:
            recent_sent = recent_sent.head(10)
            for _, row in recent_sent.iterrows():
                report += f"- {row['domain']} ({row['owner_email']}) on {row.get('email_sent_date', 'N/A')}\n"
    else:
        # Use basic csv if pandas not available
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
        
        # Domain statistics
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

=== DOMAIN DISTRIBUTION ===
"""
        for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"{domain}: {count}\n"
        
        report += "\n=== EMAIL DOMAIN DISTRIBUTION ===\n"
        for email, count in sorted(email_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"{email}: {count}\n"
        
        report += "\n=== RECENT SENT EMAILS ===\n"
        recent_sent = [r for r in rows if r.get('status','').lower() == 'sent']
        recent_sent.sort(key=lambda r: r.get('email_sent_date', ''), reverse=True)
        for row in recent_sent[:10]:
            report += f"- {row['domain']} ({row['owner_email']}) on {row.get('email_sent_date', 'N/A')}\n"
    
    # Save report
    report_path = BASE / 'prospectos' / 'outreach-summary-report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report saved to: {report_path}")
    print(report)

if __name__ == '__main__':
    main()