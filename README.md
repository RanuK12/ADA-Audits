<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RanuK12/ADA-Audits/main/assets/ranukita-logo.png">
    <img src="https://raw.githubusercontent.com/RanuK12/ADA-Audits/main/assets/ranukita-logo.png" alt="ADA Audits by Ranuk IT Solutions" width="180">
  </picture>
</p>

<h1 align="center">ADA Audits 🛡️</h1>

<p align="center">
  <strong>Automated Digital Accessibility Auditing Engine</strong><br>
  WCAG 2.1 AA compliance scanning, AI-powered reporting, and outbound sales automation.
</p>

<p align="center">
  <a href="https://github.com/RanuK12/ADA-Audits/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License MIT"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+"></a>
  <a href="https://nodejs.org"><img src="https://img.shields.io/badge/node-%3E%3D18-brightgreen" alt="Node >=18"></a>
  <a href="https://ranuk.dev"><img src="https://img.shields.io/badge/website-ranuk.dev-purple" alt="Website"></a>
</p>

---

## 📋 Table of Contents

- [Description](#-description)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🚀 Description

**ADA Audits** is a professional-grade automated ecosystem engineered to perform digital accessibility audits (ADA / WCAG 2.1 AA) for businesses, with a primary focus on the US market.

The system transforms a complex manual process into a streamlined, predictable outbound sales machine. It handles everything from **lead identification** and **automated scanning** to the generation of **branded, high-quality PDF reports**, enabling a scalable consulting workflow.

Built for agencies, accessibility consultants, and SaaS teams who need to deliver compliance audits at scale without the overhead of manual testing.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Lead Screening** | Rapid 30-second scans to filter viable targets from a URL list |
| **Full Audit Pipeline** | Automated deep scans, score calculation, and branded PDF generation |
| **AI-Powered Synthesis** | Claude 3.5 Sonnet integration to turn raw scan data into human-readable insights |
| **Compliance Scoring** | Standalone score calculation engine (WCAG 2.1 AA criteria) |
| **Batch Processing** | Scan hundreds of domains in a single run |
| **Telegram Notifications** | Real-time alerts on scan completion and errors |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Scanning Engines** | `axe-core CLI`, `Lighthouse`, `Puppeteer` |
| **Automation** | `Python 3`, `Bash` |
| **Report Generation** | `WeasyPrint` (branded PDFs), `Jinja2` templates, `Markdown` |
| **AI Integration** | `Claude 3.5 Sonnet` (synthesis & analysis) |
| **Notifications** | `Telegram Bot API` |

---

## 📦 Installation

### Prerequisites

- **Node.js** >= 18
- **Python** >= 3.10
- **pip** (Python package manager)
- **Git**

### Step 1: Clone the repository

```bash
git clone https://github.com/RanuK12/ADA-Audits.git
cd ADA-Audits
```

### Step 2: Install global Node.js tools

```bash
npm install -g @axe-core/cli puppeteer lighthouse
```

### Step 3: Install Python dependencies

```bash
pip install -r requirements.txt
```

If no `requirements.txt` exists, install core packages:

```bash
pip install weasyprint jinja2 requests
```

### Step 4: Verify installation

```bash
axe --version
lighthouse --version
python3 -c "import weasyprint; print('WeasyPrint OK')"
```

---

## 📖 Usage

### 1. Quick Lead Screening

Determine if a website is a viable lead in seconds:

```bash
./scripts/quick-scan.sh https://example.com
```

Batch processing from a file:

```bash
./scripts/quick-scan.sh -f prospectos/urls-del-dia.txt
```

### 2. Full Audit Pipeline (The "Gold" Path)

Run the complete flow — scan → score → branded PDF:

**One-liner:**

```bash
./scripts/quick-audit.sh https://example.com "Company Name"
```

**Step-by-step (manual):**

```bash
python3 scripts/audit-pipeline.py https://example.com --company "Company Name"
```

### 3. Compliance Score Calculation

Calculate a standalone score from a raw JSON output:

```bash
python3 scripts/compliance_score.py entregables/domain_com/axe-raw.json
```

### 4. Generate a Branded PDF Report

```bash
python3 scripts/generate_report.py --domain example.com --score 72 --output report.pdf
```

---

## 📂 Project Structure

```text
ADA-AUDITS/
├── README.md                   # Project documentation
├── FLUJO-DIARIO.md             # Daily routine & operational guide
├── CHEATSHEET-BOT.md           # Quick commands reference
├── LICENSE                     # MIT license
├── pyproject.toml              # Python project config
├── netlify.toml                # Netlify deploy config
├── scripts/                    # Core automation engine
│   ├── quick-scan.sh           # Lead screening script
│   ├── quick-audit.sh          # Full audit pipeline
│   ├── audit-pipeline.py       # Python audit orchestrator
│   ├── compliance_score.py     # Score calculation engine
│   └── generate_report.py      # PDF report generator
├── templates/                  # Audit templates & AI prompts
├── prospectos/                 # Targeting criteria & lead pipeline
├── entregables/                # Sample audit deliverables
├── landing/                    # Landing page assets
├── tests/                      # Test suite
└── logs/                       # Execution & error logs
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Commit your changes**: `git commit -m 'feat: add your feature'`
4. **Push to the branch**: `git push origin feature/your-feature`
5. **Open a Pull Request**

### Guidelines

- Follow existing code style and conventions
- Add tests for new functionality
- Keep PRs focused — one feature/fix per PR
- Update documentation when changing behavior
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages

### Reporting Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/RanuK12/ADA-Audits/issues) with a clear description and reproduction steps.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- **Website**: [ranuk.dev](https://ranuk.dev)
- **GitHub**: [RanuK12](https://github.com/RanuK12)
- **Email**: emilio@ranuk.dev
- **Project Repo**: [github.com/RanuK12/ADA-Audits](https://github.com/RanuK12/ADA-Audits)

---

<p align="center">
  <sub>
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RanuK12/ADA-Audits/main/assets/minilogo2.png">
      <img src="https://raw.githubusercontent.com/RanuK12/ADA-Audits/main/assets/minilogo2.png" alt="Ranuk IT Solutions" width="24" style="vertical-align: middle;">
    </picture>
    &nbsp;Developed by <strong>Ranuk IT Solutions</strong>
  </sub>
  <br>
  <sub><a href="https://ranuk.dev">ranuk.dev</a> · <a href="https://github.com/RanuK12">GitHub</a></sub>
</p>
