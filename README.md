# ADA Audits

## Project Overview
ADA Audits is a professional-grade automated system designed to perform digital accessibility audits (ADA / WCAG 2.1 AA) for businesses, primarily in the US market. The system streamlines the entire workflow from lead identification to the generation of branded, high-quality audit reports.

By combining automated scanning, market intelligence, and custom-tailored email templates, ADA Audits enables a predictable outbound sales process to secure high-value accessibility consulting contracts.

## Tech Stack
- **Scanning Engines:** axe-core CLI, Lighthouse, Puppeteer
- **Scripting & Automation:** Bash, Python 3
- **Report Generation:** WeasyPrint (branded PDFs), Jinja2 templates, Markdown
- **AI Integration:** Claude Sonnet 4 (for final report synthesis)
- **Communication:** Gmail API / Manual Outbound, Telegram Bot for notifications

## Installation Guide

### Prerequisites
Ensure you have Node.js and Python 3 installed on your system.

### Initial Setup
Run the following commands to install the necessary scanning tools globally:

```bash
npm i -g @axe-core/cli puppeteer lighthouse
```

### Verification
Verify the installations by checking the versions:
```bash
axe --version
lighthouse --version
```

## Usage Examples

### Quick Lead Screening
To quickly determine if a website is a viable lead (30-second scan):
```bash
./scripts/quick-scan.sh https://example.com
```
To process a batch of URLs from a file:
```bash
./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt
```

### Full Audit Pipeline
To run the complete automated pipeline (Scan -> Score -> Branded PDF):

**One-liner:**
```bash
./scripts/quick-audit.sh https://example.com "Company Name"
```

**Step-by-step execution:**
```bash
python3 scripts/audit-pipeline.py https://example.com --company "Company Name"
```

### Compliance Score Calculation
To calculate a standalone compliance score from a raw JSON file:
```bash
python3 scripts/compliance-score.py entregables/domain_com/axe-raw.json
```

## Project Structure
```
ADA-AUDITS/
├── README.md                   # Project documentation
├── FLUJO-DIARIO.md             # Daily routine guide
├── CHEATSHEET-BOT.md           # Quick commands for the bot
├── templates/                  # Audit templates and prompts
├── scripts/                    # Core automation scripts
├── prospectos/                 # Targeting criteria and lead pipeline
├── entregables/                # Sample audit deliverables
└── logs/                       # Execution logs
```