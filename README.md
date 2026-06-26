# ADA Audits 🛡️

> **Automated WCAG 2.1 AA accessibility audits for US businesses.**
> Turn compliance risk into revenue — scan, score, pitch, report, close.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)](https://nodejs.org/)

---

## 💼 The Business Problem

Every year, **4,000+ ADA website accessibility lawsuits** are filed in the US. The average settlement costs **$15,000–$50,000**, and a full remediation runs **$10,000–$30,000**. Yet **97% of homepages** have detectable WCAG failures ([WebAIM Million](https://webaim.org/projects/million/)).

Most business owners:
- Don't know they're at risk
- Can't afford $5k–$15k manual audits from agencies
- Need a fast, credible report to show compliance efforts

**ADA Audits fills that gap** — automated, affordable ($899–$1,499), and delivered in 48 hours.

---

## 🚀 What It Does

ADA Audits is a complete outbound sales + delivery engine for accessibility compliance services:

| Stage | What Happens | Tool |
|-------|-------------|------|
| **1. Lead Screening** | Scan 20 URLs in 5 min. Filter by score, issues, and vertical. | `quick-scan.sh` |
| **2. Pitch Generation** | Auto-generate personalized cold emails referencing real issues. | `generate-pitch.py` |
| **3. Full Audit** | Deep scan (axe-core + Lighthouse), compliance score, AI synthesis. | `audit-pipeline.py` |
| **4. Branded Report** | Professional PDF with findings, legal risk assessment, and fix roadmap. | WeasyPrint + Jinja2 |
| **5. Follow-up** | CRM tracking, automated follow-ups, close management. | `leads.csv` + `next-action.py` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Scanning** | `axe-core CLI`, `Lighthouse`, `Puppeteer` |
| **Automation** | `Python 3.10+`, `Bash` |
| **Reporting** | `WeasyPrint` (PDF), `Jinja2` templates, `Markdown` |
| **AI** | `Claude 3.5 Sonnet` (synthesis, analysis, pitch writing) |
| **Notifications** | `Telegram Bot` API |
| **CLI** | Unified `ada` command (`python -m scripts`) |

---

## 📦 Quick Start

### Prerequisites

```bash
# Node.js 18+ and Python 3.10+
npm i -g @axe-core/cli puppeteer lighthouse
```

### Verify

```bash
axe --version
lighthouse --version
```

### Scan a Site in 5 Seconds

```bash
./scripts/quick-scan.sh https://example.com
```

### Batch Scan (20 URLs)

```bash
./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt
```

### Full Audit → PDF

```bash
./scripts/quick-audit.sh https://example.com "Company Name"
```

### Generate a Cold Pitch

```bash
python3 scripts/generate-pitch.py https://example.com
```

### Unified CLI

```bash
python -m scripts scan entregables/domain_com/axe-raw.json
python -m scripts version
```

---

## 📊 Sample Output

```json
{
  "url": "https://example.com",
  "wcag_compliance_score": 42,
  "total_violations": 28,
  "by_severity": {
    "critical": 3,
    "serious": 12,
    "moderate": 8,
    "minor": 5
  },
  "legal_risk": "HIGH — multiple critical violations expose to ADA litigation",
  "recommendation": "Immediate remediation recommended. Focus on missing alt text, insufficient color contrast, and keyboard navigation gaps."
}
```

---

## 💰 Business Model & Pricing

| Service | Price | Delivery |
|---------|-------|----------|
| **Quick Scan + Pitch** (lead gen) | Free (inbound) | 5 min |
| **Full WCAG 2.1 AA Audit** | $899–$1,499 | 48 hours |
| **Audit + Remediation** | $2,499–$4,999 | 1–2 weeks |
| **Monthly Compliance Monitoring** | $499/mo | Ongoing |

**Target verticals:** Dentists, chiropractors, boutique hotels, law firms, restaurants, e-commerce.

**Market size:** ~15M US small businesses with websites. At 1% conversion → 150k audits × $1k avg = **$150M TAM**.

---

## 📂 Project Structure

```
ADA-AUDITS/
├── README.md                  # This file
├── FLUJO-DIARIO.md            # Daily 2-hour routine
├── CHEATSHEET-BOT.md          # Telegram bot commands
├── pyproject.toml             # Python project config
├── netlify.toml               # Landing page deploy config
│
├── scripts/                   # Core automation engine
│   ├── ada                    # Global CLI symlink
│   ├── __main__.py            # Unified entry point
│   ├── quick-scan.sh          # axe-core wrapper
│   ├── quick-audit.sh         # Full pipeline one-liner
│   ├── audit-pipeline.py      # Scan → score → PDF
│   ├── compliance_score.py    # Score calculation engine
│   ├── generate-pitch.py      # Cold email generator
│   ├── generate-report.py     # AI-powered report writer
│   ├── next-action.py         # Daily action recommender
│   ├── find-emails.py         # Email discovery
│   ├── find-urls.py           # URL discovery
│   ├── fetch-site.sh          # Site downloader
│   ├── daily-auto.py          # Auto-pilot mode
│   ├── outbox.py              # Email queue manager
│   └── tg-send.py             # Telegram sender
│
├── templates/                 # Audit & email templates
├── prospectos/                # Lead pipeline & targeting
├── entregables/               # Sample deliverables
├── landing/                   # Public-facing website
├── tests/                     # Test suite
└── logs/                      # Execution logs
```

---

## 🔄 Daily Workflow (2 hours/day)

| Time | Task | Duration |
|------|------|----------|
| 🌅 Morning | Scan 20 new URLs → filter leads | 45 min |
| ☀️ Afternoon | Send 15 personalized emails | 45 min |
| 🌙 Evening | Follow-ups + replies | 30 min |

**Target:** 75 emails/week → 6–10 replies → 1–2 closes → **$1,600–$2,400/week**.

See [`FLUJO-DIARIO.md`](FLUJO-DIARIO.md) for the complete daily routine.

---

## 🤖 Telegram Bot Commands

All operations available via Telegram:

| Command | Action |
|---------|--------|
| `ada scan <url>` | Scan single site |
| `ada scan-batch` | Scan today's URLs |
| `ada pitch <url>` | Generate cold email |
| `ada report <url>` | Full AI audit report |
| `ada next` | What to do now |
| `ada status` | Pipeline summary |
| `ada add-lead <url> <email>` | Log a lead |

---

## 🌐 Landing Page

The public-facing site lives at [`landing/`](landing/) and deploys to [ada-audits.com](https://ada-audits.com) via Netlify.

```bash
# Deploy
cd landing && netlify deploy --prod
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 📄 License

MIT — see [`LICENSE`](LICENSE).

---

## 🏢 About

Built and operated by **Ranuk IT Solutions**.

- Web: [ranuk.dev](https://ranuk.dev)
- Email: hello@ada-audits.com
- Service: [ada-audits.com](https://ada-audits.com)

---

*Turn compliance into revenue. One scan at a time.*
