# ADA-Audits

Automated Data Accessibility Audits for Python projects.

## 📌 Features
- Scans Python files and notebooks for data accessibility issues
- Detects missing docstrings, type hints, and accessibility standards
- Generates reports with actionable insights
- Integrates with CI/CD pipelines

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Poetry (recommended)

### Installation
```bash
# Using pip
pip install -e .

# Using Poetry
poetry install
```

### Basic Usage
```bash
# Scan a single file
ada-scan path/to/file.py

# Scan a directory
ada-scan path/to/directory

# Generate report
ada-audit --output report.md
```

## 🔧 Configuration

Create a `.ada-audit.yml` file in your project root:

```yaml
targets:
  - src/
  - notebooks/

rules:
  - missing-docstring
  - missing-type-hint
  - accessibility-issue

output:
  format: markdown
  file: audit-report.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add new rule [ranukita:xxxxx]'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.