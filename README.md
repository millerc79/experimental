# Experimental - Learning & Automation Projects

Welcome! This is a beginner-friendly repository for exploring programming, building automation tools, and learning by doing.

## Main Project: PDF Automation Tool

A smart, local alternative to Hazel for automating PDF organization. Automatically processes, renames, and organizes PDF files by reading their content.

### Key Features

- 🔍 **Smart Year Detection** - Automatically extracts years from PDF content (no yearly rule updates!)
- 📅 **Date Extraction** - Pulls dates from PDFs for intelligent renaming
- 📁 **Auto-Organization** - Moves files to year-based folders in your Filing Cabinet
- 🔒 **100% Local** - Runs entirely on your Mac, no cloud services
- 🧪 **Dry-Run Mode** - Preview changes before applying them
- ✅ **Secure** - Comprehensive security analysis and safe file operations

### Quick Start

See [MAC_SETUP.md](MAC_SETUP.md) for detailed setup instructions.

```bash
# 1. Install dependency
pip3 install PyPDF2

# 2. Set up your configuration (first time only)
cp run_incoming_scans_template.sh run_incoming_scans.sh
cp pdf_rules_example.json pdf_rules_filing_cabinet.json
# Edit both files with your paths

# 3. Test with dry-run (safe, no files moved)
./run_incoming_scans.sh dry-run

# 4. Process files once
./run_incoming_scans.sh once

# 5. Watch continuously
./run_incoming_scans.sh watch
```

### How It Works

**Your Setup:**
- **Source:** `~/Library/Mobile Documents/com~apple~CloudDocs/Incoming Scans`
- **Destination:** `~/Documents/Filing Cabinet/{year}/{category}/`

**Example:**
1. You scan an App Store receipt dated "January 15, 2025"
2. Scanner saves it as `IMG_1234.pdf` to Incoming Scans
3. Tool reads the PDF, finds "receipt" and "iCloud" keywords
4. Tool extracts date: "January 15, 2025" from PDF content
5. Tool renames to: `App Store_2025-01-15_2025.pdf`
6. Tool moves to: `Filing Cabinet/2025/Receipts/`

**And it works for 2026, 2027, 2028... automatically!** No need to update rules every year like Hazel.

### Documentation

- 📖 [MAC_SETUP.md](MAC_SETUP.md) - Complete setup guide for Mac
- 📁 [FILING_CABINET_STRUCTURE.md](FILING_CABINET_STRUCTURE.md) - How files are organized
- 🔒 [SECURITY_ANALYSIS.md](SECURITY_ANALYSIS.md) - Security audit and best practices
- ✅ [CODE_VALIDATION_CHECKLIST.md](CODE_VALIDATION_CHECKLIST.md) - Essential checks for any code
- 🔧 [PERMISSIONS_GUIDE.md](PERMISSIONS_GUIDE.md) - How file permissions work
- 📝 [FILENAME_HANDLING.md](FILENAME_HANDLING.md) - Filename sanitization details
- 🤖 [CLAUDE_CODE_AUTOMATION.md](CLAUDE_CODE_AUTOMATION.md) - Using with Claude Code

### Pre-Configured Rules

Default rules for common document types:
- App Store receipts → `{year}/Receipts/`
- Bank statements → `{year}/Banking/Statements/`
- Credit card statements → `{year}/Banking/Credit Cards/`
- Invoices → `{year}/Invoices/`
- Tax documents → `{year}/Taxes/`
- Utility bills → `{year}/Bills/Utilities/`
- Medical documents → `{year}/Medical/`
- Insurance documents → `{year}/Insurance/`

Customize by editing `pdf_rules_filing_cabinet.json`

---

## Other Projects

### File Organizer (`file_organizer.py`)

A simple beginner script that organizes messy folders by sorting files into categories.

**Features:**
- **Images** → .jpg, .png, .gif, etc.
- **Documents** → .pdf, .docx, .txt, etc.
- **Videos** → .mp4, .avi, .mov, etc.
- **Music** → .mp3, .wav, etc.
- **Archives** → .zip, .rar, etc.
- **Code** → .py, .js, .html, etc.
- **Other** → anything that doesn't fit above

**Run it:**
```bash
python3 file_organizer.py
```

Great for learning Python basics: functions, loops, conditionals, file operations, and dictionaries.

---

## Repository Structure

```
Experimental/
├── README.md                          # You are here
├── CLAUDE.MD                          # Instructions for Claude Code
├── pdf_automation.py                  # Main PDF automation script
├── run_incoming_scans.sh              # Easy launcher script
├── pdf_rules_filing_cabinet.json      # Your PDF organization rules
├── requirements.txt                   # Python dependencies
│
├── docs/                              # Documentation
│   ├── MAC_SETUP.md
│   ├── FILING_CABINET_STRUCTURE.md
│   ├── SECURITY_ANALYSIS.md
│   ├── PERMISSIONS_GUIDE.md
│   ├── FILENAME_HANDLING.md
│   ├── CODE_VALIDATION_CHECKLIST.md
│   └── CLAUDE_CODE_AUTOMATION.md
│
└── file_organizer.py                  # Simple file organizer (beginner project)
```

---

## Getting Help

- **Setup issues?** See [MAC_SETUP.md](MAC_SETUP.md) troubleshooting section
- **Security questions?** Read [SECURITY_ANALYSIS.md](SECURITY_ANALYSIS.md)
- **Want to customize?** Edit `pdf_rules_filing_cabinet.json` and test with `--dry-run`
- **Using Claude Code?** See [CLAUDE_CODE_AUTOMATION.md](CLAUDE_CODE_AUTOMATION.md)

---

## Philosophy

This repository follows these principles:
- **Learning-focused** - Code is for learning, not perfection
- **Safety first** - Comprehensive error handling and security
- **Local processing** - No cloud services, your data stays private
- **Well-documented** - Extensive guides for understanding and customization
- **Beginner-friendly** - Clear explanations and step-by-step instructions

See [CLAUDE.MD](CLAUDE.MD) for the complete code quality standards applied to this project.

---

**Remember**: Programming is learning by doing. Play with the code, break it, fix it, and make it yours!
