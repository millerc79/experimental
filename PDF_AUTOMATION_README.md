# PDF Automation Tool 🚀

A smart, local alternative to Hazel for automating PDF organization. **No more updating rules every year!**

## The Problem This Solves

In Hazel, you need to create separate rules for each year:
- "App Receipt 2019"
- "App Receipt 2020"
- "App Receipt 2021"
- "App Receipt 2022"
- "App Receipt 2023"
- "App Receipt 2024"
- "App Receipt 2025"
- ...and so on forever 😫

**This tool automatically detects years from PDF content**, so you write the rule once and it works forever!

## Key Features

✅ **Smart Year Detection** - Automatically finds years in PDF content
✅ **Date Extraction** - Pulls dates from PDFs for smart renaming
✅ **Rule-Based System** - Define rules once, use forever
✅ **Local Processing** - Runs entirely on your computer
✅ **Dry Run Mode** - Preview changes before applying them
✅ **Pattern Matching** - Match PDFs by keywords in content
✅ **Auto-Organize** - Rename and move files automatically

## Installation

### Step 1: Install Python (if needed)
This tool requires Python 3.7 or higher. Check if you have it:
```bash
python3 --version
```

### Step 2: Install Required Library
```bash
pip install PyPDF2
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Run the Tool
```bash
python3 pdf_automation.py
```

On first run, it will create a sample `pdf_rules.json` file for you.

### 2. Try a Dry Run
When prompted:
- Enter the folder path with PDFs (or press Enter for current folder)
- Choose "y" for dry run to preview what will happen

### 3. Run for Real
Run again and choose "n" for dry run to actually move and rename files.

## How Rules Work

Rules are stored in `pdf_rules.json`. Each rule has:

### Conditions (when to apply the rule)
- `extension`: File type (usually "pdf")
- `content_contains`: Keywords that must appear in the PDF

### Actions (what to do)
- `rename_pattern`: How to rename the file
- `move_to`: Folder to move the file to

### Example Rule
```json
{
  "name": "App Store Receipts",
  "conditions": {
    "extension": "pdf",
    "content_contains": ["receipt", "icloud"]
  },
  "actions": {
    "rename_pattern": "App Store_{date}_{year}{ext}",
    "move_to": "Receipts"
  }
}
```

This rule will:
1. Find PDFs containing "receipt" AND "icloud"
2. Extract the date and year from the PDF content
3. Rename to something like: `App Store_2025-01-15_2025.pdf`
4. Move to a `Receipts` folder

## Rename Pattern Variables

You can use these placeholders in `rename_pattern`:

| Variable | Description | Example |
|----------|-------------|---------|
| `{date}` | Date found in PDF | `2025-01-15` |
| `{year}` | Year found in PDF | `2025` |
| `{ext}` | File extension | `.pdf` |
| `{date_created}` | File creation date | `2025-01-15` |
| `{original_name}` | Original filename (no extension) | `receipt_123` |

## Customizing Rules

### Adding a New Rule

Edit `pdf_rules.json` and add:

```json
{
  "name": "Insurance Documents",
  "description": "Organizes insurance PDFs",
  "conditions": {
    "extension": "pdf",
    "content_contains": ["insurance", "policy"]
  },
  "actions": {
    "rename_pattern": "Insurance_{year}_{date}{ext}",
    "move_to": "Insurance"
  }
}
```

### Keywords Are Case-Insensitive
- `"receipt"` will match "Receipt", "RECEIPT", or "receipt"
- All keywords in `content_contains` must be present (AND logic)

### Multiple Destination Folders
Use `/` to create subfolders:
```json
"move_to": "Documents/Banking/Statements"
```

## Recreating Your Hazel Rules

Your Hazel rule from the screenshot would be:

```json
{
  "name": "App Receipt Auto-Year",
  "conditions": {
    "extension": "pdf",
    "content_contains": ["receipt", "icloud"]
  },
  "actions": {
    "rename_pattern": "App Store_{date}{ext}",
    "move_to": "Receipts"
  }
}
```

**That's it!** No need to create separate rules for 2024, 2025, 2026, etc. The tool automatically extracts the year from the PDF content.

## Advanced Usage

### Processing a Specific Folder
```python
from pdf_automation import PDFAutomation

automation = PDFAutomation()
automation.process_folder("/path/to/downloads", dry_run=True)
```

### Custom Rules File
```python
automation = PDFAutomation(rules_file="my_custom_rules.json")
```

## Automating with Cron (Linux/Mac)

To run automatically every hour:

1. Open crontab:
```bash
crontab -e
```

2. Add this line (adjust paths):
```
0 * * * * cd /home/user/Experimental && python3 pdf_automation.py
```

## Automating with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\pdf_automation.py`

## Troubleshooting

### "PyPDF2 not installed" Error
Run: `pip install PyPDF2`

### PDFs Not Being Processed
- Check that keywords in rules match PDF content (case-insensitive)
- Try dry run mode to see what's detected
- Make sure PDFs contain readable text (not scanned images)

### No Date/Year Detected
- The tool will use the current year as fallback
- Check PDF content - dates should be in common formats
- File creation date is always available as `{date_created}`

## How It's Better Than Hazel

| Feature | Hazel | PDF Automation Tool |
|---------|-------|---------------------|
| Auto year detection | ❌ Need separate rules per year | ✅ Automatic |
| Extract dates from PDFs | ❌ Use file dates only | ✅ Reads PDF content |
| Free | ❌ $42 | ✅ Free & open source |
| Cross-platform | ❌ Mac only | ✅ Windows, Mac, Linux |
| Customizable | ⚠️ GUI limitations | ✅ Full Python code access |
| Dry run preview | ✅ | ✅ |

## Learning Resources

- **Python file operations**: [Real Python - Working with Files](https://realpython.com/working-with-files-in-python/)
- **Regular expressions**: [RegexOne Tutorial](https://regexone.com/)
- **JSON format**: [JSON.org](https://www.json.org/)

## Next Steps

1. ✅ Install PyPDF2
2. ✅ Run with dry mode to test
3. ✅ Customize rules for your needs
4. ✅ Set up automation (cron/Task Scheduler)
5. ✅ Enjoy not updating rules every year! 🎉

## Need Help?

- Check the code comments in `pdf_automation.py` - it's heavily documented
- Try the example rules in `pdf_rules_example.json`
- Experiment with dry run mode first

---

**Made with ❤️ for learning and automation**
