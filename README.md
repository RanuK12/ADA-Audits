# ADA-Audits

Automated Data Accessibility Audits for Python projects.

## 📌 Features

- Scans Python files and notebooks for data accessibility issues
- Detects missing docstrings, type hints, and accessibility standards
- Generates reports with actionable insights
- Integrates with CI/CD pipelines

## 🚀 Quick Start

Follow these steps to get started with ADA-Audits:

### Step 1: Installation

**Using pip:**

```bash
# Clone the repository
git clone https://github.com/your-org/ada-audits.git
cd ada-audits

# Install in development mode
pip install -e .
```

**Using Poetry:**

```bash
# Clone the repository
git clone https://github.com/your-org/ada-audits.git
cd ada-audits

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Step 2: Create Configuration File

Create a `.ada-audit.yml` file in your project root:

```yaml
# .ada-audit.yml - Minimal working configuration
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

### Step 3: Run Your First Audit

**Scan a single file:**

```bash
ada-scan path/to/file.py
```

Expected output:
```
✓ Scanning: path/to/file.py
Found 3 issues:
  [WARNING] line 15: Missing docstring for function 'process_data'
  [WARNING] line 23: Missing type hint for parameter 'input_path'
  [ERROR]   line 45: Accessibility issue - missing alt text for image
```

**Scan an entire directory:**

```bash
ada-scan src/
```

Expected output:
```
✓ Scanning directory: src/
Found 12 files to analyze
  src/__init__.py .............. OK
  src/main.py .................. 2 issues
  src/utils.py ................. 5 issues
  src/processors/base.py ....... 1 issue
  src/processors/transform.py .. 4 issues

Summary: 12 issues found across 4 files
```

**Generate a full report:**

```bash
ada-audit --output report.md
```

Expected output:
```
✓ ADA Audit Report Generated
  Output: report.md
  Total files scanned: 12
  Issues found: 15
  Compliance score: 78%
```

## 📖 Usage

### Command Line Interface

| Command | Description |
|---------|-------------|
| `ada-scan <path>` | Scan a file or directory for accessibility issues |
| `ada-audit` | Generate a full audit report based on configuration |
| `ada-audit --output <file>` | Generate report with custom output filename |
| `ada-audit --format <fmt>` | Output format: `markdown`, `json`, or `html` |

### Configuration Reference

Full configuration options for `.ada-audit.yml`:

```yaml
# Paths to scan
targets:
  - src/              # Python source files
  - notebooks/        # Jupyter notebooks
  - tests/            # Test files

# Rules to apply
rules:
  - missing-docstring      # Functions/classes without docstrings
  - missing-type-hint      # Parameters without type annotations
  - accessibility-issue    # Accessibility standard violations

# Output settings
output:
  format: markdown         # Options: markdown, json, html
  file: audit-report.md   # Output filename

# Optional: Exclude patterns
exclude:
  - "**/__pycache__/**"
  - "**/migrations/**"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add new rule [ranukita:xxxxx]'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# Ultimo update: Tue Sep  8 00:18:27 CEST 2026
