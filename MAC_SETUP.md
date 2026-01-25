# Mac Setup Guide - Incoming Scans Automation

This guide helps you set up automated PDF processing for your iCloud "Incoming Scans" folder on your Mac.

## Your Setup

**Watched Folder (Source)**:
```
/Users/chadmiller/Library/Mobile Documents/com~apple~CloudDocs/Incoming Scans
```

**Filing Cabinet (Destination)**:
```
/Users/chadmiller/Documents/Filing Cabinet
```

This setup will:
- Monitor your "Incoming Scans" folder for new PDFs
- Read PDF content to identify document types
- Extract dates and years from PDF content (not filename!)
- Rename with standardized patterns
- Organize into Filing Cabinet by **year** and **category**

📖 **See [FILING_CABINET_STRUCTURE.md](FILING_CABINET_STRUCTURE.md) for complete folder organization details**

## Quick Start (On Your Mac)

### 1. First, clone this repository to your Mac

```bash
cd ~/Documents  # or wherever you want to keep it
git clone https://github.com/millerc79/Experimental.git
cd Experimental
```

### 2. Install PyPDF2

```bash
pip3 install PyPDF2
```

Or use the requirements file:
```bash
pip3 install -r requirements.txt
```

### 3. Test with Dry Run (Safe!)

This shows what would happen WITHOUT actually moving files:

```bash
./run_incoming_scans.sh dry-run
```

This will:
- Check your Incoming Scans folder for PDFs
- Show what rules would match
- Show what the files would be renamed to
- Show where they would be moved
- **But NOT actually move anything**

### 4. Process Once

If the dry run looks good, process the current files:

```bash
./run_incoming_scans.sh once
```

### 5. Start Watching (Continuous Monitoring)

To continuously monitor for new PDFs:

```bash
./run_incoming_scans.sh watch
```

This will:
- Check every 30 seconds for new PDFs
- Automatically process them based on your rules
- Keep running until you press Ctrl+C

## Customizing Rules

Edit `pdf_rules_filing_cabinet.json` to customize what happens to your PDFs.

This file is specifically configured for your Filing Cabinet setup with year-based organization.

**Default rules included:**
- App Store receipts → `Receipts/` folder
- Bank statements → `Banking/Statements/` folder
- Invoices → `Invoices/` folder
- Tax documents → `Taxes/` folder
- Utility bills → `Bills/Utilities/` folder

### Example: Add a Rule for Subscription Receipts

Edit `pdf_rules_filing_cabinet.json` and add:

```json
{
  "name": "Subscription Receipts",
  "description": "Organizes monthly subscription payments",
  "conditions": {
    "extension": "pdf",
    "content_contains": ["subscription", "recurring"]
  },
  "actions": {
    "rename_pattern": "Subscription_{date}{ext}",
    "move_to": "/Users/chadmiller/Documents/Filing Cabinet/{year}/Subscriptions"
  }
}
```

**Note the `{year}` placeholder** - it gets replaced with the actual year from the PDF!

Then test:
```bash
./run_incoming_scans.sh dry-run
```

## Running Automatically on Startup

To have this run automatically when you log into your Mac:

### Option 1: Create a LaunchAgent (Recommended)

1. Create a plist file:

```bash
nano ~/Library/LaunchAgents/com.chadmiller.pdfautomation.plist
```

2. Paste this content (update the path to where you cloned the repo):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.chadmiller.pdfautomation</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/chadmiller/Documents/Experimental/run_incoming_scans.sh</string>
        <string>watch</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/chadmiller/pdf_automation.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/chadmiller/pdf_automation_error.log</string>
</dict>
</plist>
```

3. Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.chadmiller.pdfautomation.plist
```

4. To stop it:

```bash
launchctl unload ~/Library/LaunchAgents/com.chadmiller.pdfautomation.plist
```

### Option 2: Add to Login Items

1. Open System Settings → General → Login Items
2. Click the "+" button
3. Navigate to and select `run_incoming_scans.sh`
4. Make sure it's set to run at login

**Note**: This method shows the terminal window. Use LaunchAgent for background operation.

## Monitoring and Logs

### Check if it's running:

```bash
ps aux | grep pdf_automation
```

### View logs (if using LaunchAgent):

```bash
tail -f ~/pdf_automation.log
```

### Manual check of what's being processed:

```bash
./run_incoming_scans.sh dry-run
```

## Folder Structure

After processing, PDFs are moved from "Incoming Scans" to your "Filing Cabinet" organized by year:

```
/Users/chadmiller/Documents/Filing Cabinet/
├── 2024/
│   ├── Receipts/
│   ├── Banking/
│   │   ├── Statements/
│   │   └── Credit Cards/
│   ├── Invoices/
│   ├── Taxes/
│   ├── Bills/
│   │   └── Utilities/
│   ├── Medical/
│   └── Insurance/
└── 2025/
    ├── Receipts/
    │   ├── App Store_2025-01-15_2025.pdf
    │   └── App Store_2025-01-20_2025.pdf
    ├── Banking/
    │   ├── Statements/
    │   │   └── Bank_Statement_2025-01-01.pdf
    │   └── Credit Cards/
    ├── Invoices/
    │   └── Invoice_2025-01-10_2025.pdf
    ├── Taxes/
    ├── Bills/
    │   └── Utilities/
    │       └── Utility_Bill_2025-01-05.pdf
    ├── Medical/
    └── Insurance/
```

**Key feature:** Year is detected from PDF content, not the filename or scan date!

## Troubleshooting

### "Incoming Scans folder not found"

Check that:
1. iCloud Drive is enabled and syncing
2. The folder exists in iCloud Drive
3. The path is correct (check in Finder: Go → Go to Folder → paste the path)

### "PyPDF2 not installed"

Run:
```bash
pip3 install PyPDF2
```

If `pip3` isn't found:
```bash
python3 -m pip install PyPDF2
```

### PDFs aren't being processed

1. Check that they contain searchable text (not scanned images)
2. Run dry-run to see what's detected
3. Check the rules in `pdf_rules.json`
4. Look at the logs

### Want to stop automatic processing

```bash
# If using LaunchAgent:
launchctl unload ~/Library/LaunchAgents/com.chadmiller.pdfautomation.plist

# If running manually, just press Ctrl+C
```

## Testing the Setup

Put a test PDF in your Incoming Scans folder and run:

```bash
./run_incoming_scans.sh dry-run
```

You should see output showing:
- PDF was found
- What keywords were matched
- What the new name would be
- Where it would be moved

## Command Reference

| Command | What It Does |
|---------|--------------|
| `./run_incoming_scans.sh dry-run` | Preview changes (safe) |
| `./run_incoming_scans.sh once` | Process current PDFs |
| `./run_incoming_scans.sh watch` | Monitor continuously |
| `./run_incoming_scans.sh` | Same as `watch` (default) |

## Next Steps

1. ✅ Clone repo to your Mac
2. ✅ Install PyPDF2
3. ✅ Run dry-run to test
4. ✅ Customize rules in `pdf_rules.json`
5. ✅ Set up LaunchAgent for automatic startup
6. ✅ Monitor the logs to ensure it's working

---

**Pro Tip**: Start with dry-run mode and test with a few PDFs before setting up automatic processing. Once you're confident it works as expected, set up the LaunchAgent for hands-free operation!
