# file-organizer

A simple Python utility for automatically organizing files into categorized folders based on file type/extension.

## What It Does

Scans a folder and automatically moves files into organized subfolders:

- **Images** → `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`
- **Documents** → `.pdf`, `.doc`, `.docx`, `.txt`, `.xlsx`, `.pptx`
- **Videos** → `.mp4`, `.avi`, `.mov`, `.mkv`
- **Music** → `.mp3`, `.wav`, `.flac`, `.m4a`
- **Archives** → `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Code** → `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`
- **Other** → Everything else

## Quick Start

```bash
# Run the script
python3 file_organizer.py

# Enter the folder path when prompted (or press Enter to use test_folder)
```

## Example

**Before:**
```
Downloads/
├── vacation.jpg
├── report.pdf
├── song.mp3
├── video.mp4
└── random.xyz
```

**After:**
```
Downloads/
├── Images/
│   └── vacation.jpg
├── Documents/
│   └── report.pdf
├── Music/
│   └── song.mp3
├── Videos/
│   └── video.mp4
└── Other/
    └── random.xyz
```

## Features

- ✅ **Safe** - Uses `shutil.move()` for reliable file operations
- ✅ **Smart** - Skips files that already exist at destination
- ✅ **Clear** - Shows exactly what it's doing as it runs
- ✅ **Simple** - Pure Python, no external dependencies
- ✅ **Customizable** - Easy to add more file categories

## How to Use

### Option 1: Interactive Mode

```bash
python3 file_organizer.py
```

The script will ask you for the folder path.

### Option 2: Import as Module

```python
from file_organizer import organize_files

# Organize your Downloads folder
organize_files("/Users/YOUR_USERNAME/Downloads")

# Organize any folder
organize_files("/path/to/messy/folder")
```

## Customizing Categories

Edit the `file_categories` dictionary in `file_organizer.py`:

```python
file_categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Music': ['.mp3', '.wav', '.flac', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp'],
    # Add your own categories:
    'Ebooks': ['.epub', '.mobi', '.azw'],
    'Data': ['.csv', '.json', '.xml'],
}
```

## Requirements

- Python 3.x
- No external packages needed (uses built-in `os` and `shutil`)

## Safety Notes

- **Test first** - Try it on a test folder before using on important files
- **Backup recommended** - Make a backup of important folders before organizing
- **Existing files** - Won't overwrite files that already exist at the destination
- **Folders** - Only organizes files, not folders

## Use Cases

- Clean up messy Downloads folder
- Organize photos from multiple sources
- Sort project files by type
- Tidy up desktop files
- Process batch imports

## License

Open source - use however you like!

## Contributing

This is a learning project! Feel free to:
- Add more file categories
- Improve error handling
- Add features (undo, dry-run mode, etc.)
- Make it better!
