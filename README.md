# Python Automation Projects

Welcome! This repository contains automation tools to help you organize files and learn Python. 🎉

## Projects

### 1. File Organizer (`file_organizer.py`)
A simple script that organizes messy folders by sorting files into categories.

### 2. PDF Automation Tool (`pdf_automation.py`) - NEW!
A smart alternative to Hazel that automatically processes, renames, and organizes PDF files by reading their content. **No need to update rules every year!**

📖 See [PDF_AUTOMATION_README.md](PDF_AUTOMATION_README.md) for full documentation.

---

## File Organizer

The `file_organizer.py` script automatically organizes messy folders by sorting files into categories:

- **Images** → .jpg, .png, .gif, etc.
- **Documents** → .pdf, .docx, .txt, etc.
- **Videos** → .mp4, .avi, .mov, etc.
- **Music** → .mp3, .wav, etc.
- **Archives** → .zip, .rar, etc.
- **Code** → .py, .js, .html, etc.
- **Other** → anything that doesn't fit above

## How to Run It

### Step 1: Make sure Python is installed
Open a terminal and type:
```bash
python --version
```
or
```bash
python3 --version
```

You should see something like "Python 3.x.x"

### Step 2: Run the script
In your terminal, navigate to this folder and run:
```bash
python file_organizer.py
```
or
```bash
python3 file_organizer.py
```

### Step 3: Tell it which folder to organize
The script will ask you which folder to organize. You can:
- Type a folder path (like `/home/user/Downloads`)
- Just press Enter to organize the `test_folder` (which we created for practice)

## Try It Out Safely

I've created a `test_folder` with some sample files you can use to test the script without risking your real files.

## What You're Learning

This script teaches you:
1. **Functions** - Reusable blocks of code (`def organize_files()`)
2. **Loops** - Doing the same thing multiple times (`for filename in...`)
3. **Conditionals** - Making decisions (`if file_extension in extensions`)
4. **File operations** - Working with files and folders
5. **Dictionaries** - Organizing data with key-value pairs

## Customize It!

Want to make it your own? Try:
- Adding new file categories (edit the `file_categories` dictionary)
- Changing where files go
- Adding more features (like organizing by date)

## Next Steps

Once you're comfortable with this script, you can:
- Organize your real Downloads folder
- Modify it to do more complex automation
- Use it as a template for other automation tasks

---

## PDF Automation Tool (Advanced)

A more sophisticated automation tool that:
- Reads PDF content to find keywords
- Automatically extracts dates and years from PDFs
- Renames files with smart patterns
- Moves files to organized folders
- Works forever without needing yearly rule updates

**Key advantage**: Unlike tools like Hazel where you need separate rules for each year (2019, 2020, 2021...), this tool automatically detects years from PDF content!

### Quick Start
1. Install requirements: `pip install -r requirements.txt`
2. Run: `python3 pdf_automation.py`
3. Try dry run mode first to preview changes

### Example Use Case
You have App Store receipts coming into your Downloads folder. The tool will:
1. Detect they contain "receipt" and "icloud"
2. Extract the date from the PDF (like "January 15, 2025")
3. Rename to: `App Store_2025-01-15_2025.pdf`
4. Move to: `Downloads/Receipts/`

**And it works for 2026, 2027, 2028... automatically!**

📖 **Full documentation**: [PDF_AUTOMATION_README.md](PDF_AUTOMATION_README.md)

---

**Remember**: Programming is learning by doing. Play with the code, break it, fix it, and make it yours!
