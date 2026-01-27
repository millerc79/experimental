# PDF Automation Tool

Smart PDF organizer - a local alternative to Hazel with intelligent year detection.

## The Problem

Tools like Hazel require separate rules for each year (2024, 2025, 2026...), meaning constant maintenance. Receipts scanned today need different rules than receipts scanned next year.

## The Solution

This tool reads PDF content and automatically extracts dates and years, organizing files by year without any rule updates. Set it up once, and it works forever.

## Key Features

- 🔍 **Smart Year Detection** - Automatically extracts years from PDF content
- 📅 **Date Extraction** - Finds dates in any format for intelligent renaming
- 📁 **Year-Based Organization** - Automatically creates `{year}/{category}/` structure
- 🔒 **100% Local** - Runs entirely on your machine, no cloud services
- 🧪 **Dry-Run Mode** - Preview changes before applying them
- ✅ **Security Audited** - Comprehensive security analysis included

## Quick Start

```bash
# 1. Install dependency
pip3 install PyPDF2

# 2. Set up your configuration
cp run_scans_template.sh run_scans.sh
cp pdf_rules_example.json pdf_rules.json
# Edit both files with your folder paths

# 3. Test with dry-run (safe, no files moved)
./run_scans.sh dry-run

# 4. Process files
./run_scans.sh once

# 5. Watch folder continuously
./run_scans.sh watch
```

## How It Works

**Example:**
1. You scan a store receipt dated "January 15, 2025"
2. Scanner saves it as `IMG_1234.pdf` to your watched folder
3. Tool reads the PDF and finds keywords: "receipt", "purchase"
4. Tool extracts the date: "2025-01-15"
5. Tool renames to: `Store_Receipt_2025-01-15_2025.pdf`
6. Tool moves to: `Documents/2025/Receipts/`

**Next year it still works** - no rule updates needed!

## Pre-Configured Rules

The tool comes with rules for common document types:

- **Store receipts** → `{year}/Receipts/`
- **Bank statements** → `{year}/Banking/Statements/`
- **Credit card statements** → `{year}/Banking/Credit Cards/`
- **Invoices** → `{year}/Invoices/`
- **Tax documents** → `{year}/Taxes/`
- **Utility bills** → `{year}/Bills/Utilities/`
- **Medical documents** → `{year}/Medical/`
- **Insurance documents** → `{year}/Insurance/`

Easy to customize by editing `pdf_rules.json`.

## Configuration

### Customize Rules

Edit `pdf_rules.json`:

```json
{
  "name": "Bank Statements",
  "conditions": {
    "extension": "pdf",
    "content_contains": ["statement", "account balance"]
  },
  "actions": {
    "rename_pattern": "Bank_Statement_{date}{ext}",
    "move_to": "/path/to/your/Documents/{year}/Banking/Statements"
  }
}
```

**Placeholders:**
- `{year}` - Extracted from PDF content (e.g., 2025)
- `{date}` - Extracted date in YYYY-MM-DD format
- `{ext}` - Original file extension (e.g., .pdf)

### Watch Folder Setup

1. Edit `run_scans.sh`
2. Set `SCANS_FOLDER` to your source folder (where PDFs arrive)
3. Set `DESTINATION_FOLDER` to where you want organized files

**Example folder structure after organization:**
```
Documents/
├── 2024/
│   ├── Receipts/
│   ├── Banking/
│   │   ├── Statements/
│   │   └── Credit Cards/
│   ├── Invoices/
│   └── Taxes/
└── 2025/
    ├── Receipts/
    │   └── Store_Receipt_2025-01-15_2025.pdf
    └── Banking/
```

## Documentation

- 📖 [MAC_SETUP.md](MAC_SETUP.md) - Complete setup guide for Mac
- 🔒 [SECURITY_ANALYSIS.md](SECURITY_ANALYSIS.md) - Security audit and best practices
- ✅ [CODE_VALIDATION_CHECKLIST.md](CODE_VALIDATION_CHECKLIST.md) - Code quality validation
- 🔧 [PERMISSIONS_GUIDE.md](PERMISSIONS_GUIDE.md) - How file permissions work
- 📝 [FILENAME_HANDLING.md](FILENAME_HANDLING.md) - Filename sanitization details

## Requirements

- **Python 3.x**
- **PyPDF2** - PDF text extraction
- **macOS** (or any Unix-like system)

## Use Cases

- Organizing scanned receipts from iCloud or scanner
- Processing bank statements by year
- Managing tax documents across multiple years
- Sorting invoices and bills automatically
- Any workflow where you need PDFs organized by year

## Safety Features

- **Dry-run mode** - See what will happen before running
- **Duplicate detection** - Won't overwrite existing files
- **Symlink protection** - Ignores symbolic links for security
- **File size limits** - Skips files over 100MB
- **Safe file operations** - Uses `shutil.move()` for atomic operations

## Running Automatically

Set up as a LaunchAgent on macOS to run automatically at startup. See [MAC_SETUP.md](MAC_SETUP.md) for instructions.

## Why I Built This

I was tired of updating Hazel rules every year. This solves that problem permanently by reading the year directly from PDF content.

## License

Open source - use however you like!

## Contributing

Issues and pull requests welcome! This started as a personal tool but can be useful for anyone dealing with year-based PDF organization.

---

**Note:** Your personal configuration files (`run_scans.sh`, `pdf_rules.json`) are gitignored. Use the template files to set up your own paths.
