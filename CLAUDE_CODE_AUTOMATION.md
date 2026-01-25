# Using Claude Code to Automate PDF Processing

This guide shows you how to use Claude Code to run your PDF automation tool automatically.

## Quick Commands for Claude Code

Just copy and paste these requests to Claude Code:

### 1. One-Time Processing (Dry Run)
```
Run the PDF automation tool on my Downloads folder in dry run mode
```

What Claude Code will do:
```bash
cd /home/user/Experimental
python3 pdf_automation.py --folder ~/Downloads --dry-run
```

### 2. One-Time Processing (Real)
```
Run the PDF automation tool on my Downloads folder and actually move the files
```

What Claude Code will do:
```bash
cd /home/user/Experimental
python3 pdf_automation.py --folder ~/Downloads
```

### 3. Watch Mode (Continuous Monitoring)
```
Start the PDF automation tool in watch mode for my Downloads folder
```

What Claude Code will do:
```bash
cd /home/user/Experimental
python3 pdf_automation.py --folder ~/Downloads --watch
```

### 4. Using the Simple Runner Script
```
Run the PDF automation runner script for my Downloads folder in dry-run mode
```

What Claude Code will do:
```bash
cd /home/user/Experimental
./run_pdf_automation.sh ~/Downloads dry-run
```

## Available Modes

### Interactive Mode (Default)
Asks you questions about what to do:
```bash
python3 pdf_automation.py
```

### Dry Run Mode
Preview what will happen without moving files:
```bash
python3 pdf_automation.py --folder ~/Downloads --dry-run
```

### Automatic Mode
Process files immediately:
```bash
python3 pdf_automation.py --folder ~/Downloads
```

### Watch Mode
Continuously monitor for new PDFs (checks every 30 seconds):
```bash
python3 pdf_automation.py --folder ~/Downloads --watch
```

Watch mode with custom interval (checks every 60 seconds):
```bash
python3 pdf_automation.py --folder ~/Downloads --watch --interval 60
```

## Common Automation Scenarios

### Scenario 1: Quick Check on New Downloads
Just say to Claude Code:
> "Check my Downloads folder for new PDFs and show me what the automation tool would do with them"

### Scenario 2: Process Everything Now
Just say to Claude Code:
> "Process all PDFs in my Downloads folder using the automation tool"

### Scenario 3: Start Background Monitoring
Just say to Claude Code:
> "Start watching my Downloads folder for new PDFs and process them automatically"

### Scenario 4: Update Rules and Test
Just say to Claude Code:
> "Edit my pdf_rules.json to add a rule for bank statements, then test it on my Downloads folder in dry run mode"

## Running in Background

To run the watch mode in the background (it keeps working even when you close the terminal):

```bash
nohup python3 pdf_automation.py --folder ~/Downloads --watch > pdf_automation.log 2>&1 &
```

To stop it later:
```bash
# Find the process
ps aux | grep pdf_automation

# Kill it (replace XXXX with the process ID)
kill XXXX
```

## Scheduling with Cron

To run automatically every hour, add to crontab:

```bash
# Edit crontab
crontab -e

# Add this line (processes Downloads folder every hour at :00)
0 * * * * cd /home/user/Experimental && python3 pdf_automation.py --folder ~/Downloads >> ~/pdf_automation_cron.log 2>&1
```

## Example Claude Code Conversations

### Example 1: First Time Setup
You: "Set up the PDF automation tool to process my Downloads folder"

Claude Code will:
1. Check if PyPDF2 is installed (install if needed)
2. Check if pdf_rules.json exists (create if needed)
3. Run a dry run to show what would happen
4. Ask if you want to proceed with actual processing

### Example 2: Adding a New Rule
You: "Add a rule to organize my utility bills. They contain 'electric' or 'water' and should go to Bills/Utilities folder"

Claude Code will:
1. Edit pdf_rules.json
2. Add the new rule
3. Run a dry run to test it
4. Show you the results

### Example 3: Troubleshooting
You: "The automation tool isn't finding dates in my PDFs, can you check what's happening?"

Claude Code will:
1. Run the tool in dry run mode with verbose output
2. Examine the PDF files to see what content is being extracted
3. Suggest fixes to the rules or date extraction logic

## Tips for Working with Claude Code

1. **Be specific about folders**: Say "Downloads folder" or "~/Documents" rather than just "files"

2. **Specify dry-run for safety**: Always good to say "dry run mode" the first time

3. **Ask for explanations**: Say "explain what this rule does" if you're unsure

4. **Request updates**: Say "update the rule for invoices to also check for 'bill'"

5. **Check status**: Ask "show me what rules are currently active"

## Command Reference

| What You Want | Command |
|---------------|---------|
| Process once (dry run) | `python3 pdf_automation.py --folder ~/Downloads --dry-run` |
| Process once (real) | `python3 pdf_automation.py --folder ~/Downloads` |
| Watch continuously | `python3 pdf_automation.py --folder ~/Downloads --watch` |
| Use custom rules file | `python3 pdf_automation.py --rules my_rules.json` |
| Check every 60 seconds | `python3 pdf_automation.py --folder ~/Downloads --watch --interval 60` |
| Interactive mode | `python3 pdf_automation.py` |
| Show help | `python3 pdf_automation.py --help` |

## Customizing for Your Workflow

Edit `pdf_rules.json` to add your own rules. Each rule needs:

```json
{
  "name": "What this rule does",
  "conditions": {
    "extension": "pdf",
    "content_contains": ["keyword1", "keyword2"]
  },
  "actions": {
    "rename_pattern": "NewName_{date}_{year}{ext}",
    "move_to": "DestinationFolder"
  }
}
```

Then test with:
```bash
python3 pdf_automation.py --folder ~/Downloads --dry-run
```

## Getting Help

Ask Claude Code:
- "How do I add a new rule for tax documents?"
- "What does the rename pattern {date} vs {date_created} mean?"
- "Show me what PDFs would be processed in my Downloads"
- "Why isn't my rule matching any files?"

---

**Pro Tip**: Start with dry run mode, verify it does what you want, then run for real. This prevents any surprises!
