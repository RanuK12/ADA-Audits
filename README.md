# ADA Audits 🛡️

## 🚀 Project Overview
**ADA Audits** is a professional-grade automated ecosystem engineered to perform digital accessibility audits (**ADA / WCAG 2.1 AA**) for businesses, with a primary focus on the US market. 

The system transforms a complex manual process into a streamlined, predictable outbound sales machine. It handles everything from **lead identification** and **automated scanning** to the generation of **branded, high-quality PDF reports**, enabling a scalable consulting workflow.

## 🛠️ Tech Stack
- **Scanning Engines:** `axe-core CLI`, `Lighthouse`, `Puppeteer`
- **Automation & Scripting:** `Python 3`, `Bash`
- **Report Generation:** `WeasyPrint` (Branded PDFs), `Jinja2` templates, `Markdown`
- **AI Integration:** `Claude 3.5 Sonnet` (Synthesis & Analysis)
- **Notifications:** `Telegram Bot` API

## 📋 Core Features & Workflow
The project is structured to move a prospect through three distinct phases:

1.  **Lead Screening:** Rapid 30-second scans to filter viable targets.
2.  **Full Audit Pipeline:** Automated execution of deep scans, score calculations, and PDF generation.
3.  **Synthesis:** AI-driven analysis to turn raw data into human-readable insights.

## 🚀 Quick Start

### Prerequisites
- **Node.js** & **Python 3**
- **Global Tools:**
  ```bash
  npm i -g @axe-core/cli puppeteer lighthouse
  ```

### Verification
```bash
axe --version
lighthouse --version
```

## 📖 Usage Guide

### 1. Quick Lead Screening
Determine if a website is a viable lead in seconds:
```bash
./scripts/quick-scan.sh https://example.com
```
*Batch processing:*
```bash
./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt
```

### 2. Full Audit Pipeline (The "Gold" Path)
Run the complete flow (Scan $\rightarrow$ Score $\rightarrow$ Branded PDF):

**One-liner:**
```bash
./scripts/quick-audit.sh https://example.com "Company Name"
```

**Manual Step-by-Step:**
```bash
python3 scripts/audit-pipeline.py https://example.com --company "Company Name"
```

### 3. Compliance Score Calculation
Calculate a standalone score from a raw JSON output:
```bash
python3 scripts/compliance-score.py entregables/domain_com/axe-raw.json
```

## 📂 Project Structure
```text
ADA-AUDITS/
├── README.md                   # Project documentation
├── FLUJO-DIARIO.md             # 📝 Daily routine & operational guide
├── CHEATSHEET-BOT.md           # 🤖 Quick commands for the bot
├── templates/                  # Audit templates and AI prompts
├── scripts/                    # Core automation engine
├── prospectos/                 # Targeting criteria & lead pipeline
├── entregables/                # Sample audit deliverables
└── logs/                       # Execution & error logs
```

## 🔄 Daily Operations
To maintain the workflow, refer to the internal documentation:
- **Daily Routine:** See `FLUJO-DIARIO.md` for the step-by-step daily execution.
- **Bot Commands:** See `CHEATSHEET-BOT.md` for quick reference.

---
*Developed by Ranuk IT Solutions | [ranuk.dev](https://ranuk.dev)*