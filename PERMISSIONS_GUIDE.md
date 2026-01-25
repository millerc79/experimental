# Permissions Guide

This guide explains how the PDF automation tool handles file permissions and what can go wrong.

## How File Operations Work

The tool uses Python's `shutil.move()` function, which works in two stages:

### Stage 1: Try to Rename (Fast)
If source and destination are on the **same filesystem**, Python does:
```python
os.rename(source, destination)  # Atomic, instant
```

This is what happens when moving within your Mac's filesystem.

### Stage 2: Copy + Delete (Fallback)
If rename fails (different filesystems or permissions), Python does:
```python
shutil.copy2(source, destination)  # Copy with metadata
os.remove(source)                   # Delete original
```

This takes longer but works across different drives/volumes.

## Required Permissions

### Source Folder (Incoming Scans)
- ✅ **Read** - To read the PDF content
- ✅ **List** - To see what files are in the folder
- ✅ **Delete** - To remove the file after moving it

### Destination Folder (Filing Cabinet)
- ✅ **Write** - To create new files
- ✅ **Execute** - To create subdirectories
- ✅ **List** - To check if file already exists

## Your Specific Setup

### Both folders are in your user directory:
```
Source:      ~/Library/Mobile Documents/.../Incoming Scans
Destination: ~/Documents/Filing Cabinet
```

**Result:** You should have **full permissions** to both locations.

### Why This Usually Works

1. Both folders are owned by you (chadmiller)
2. Both are in your home directory (`~`)
3. macOS gives you full control over your home directory
4. No sudo/admin privileges needed

## Potential Issues & Solutions

### 1. iCloud Sync Conflicts

**Problem:** iCloud is syncing a file while the tool tries to move it

**Symptoms:**
```
❌ Could not move file: [Errno 16] Resource busy
```

**Solution:**
- The tool will skip the file and continue
- File will be processed on next run
- Or wait a few seconds and try again

### 2. File Open in Another App

**Problem:** PDF is open in Preview, Adobe Reader, etc.

**Symptoms:**
```
❌ Could not move file: [Errno 1] Operation not permitted
```

**Solution:**
- Close the PDF in all applications
- Tool will process it on next run

### 3. Disk Full

**Problem:** Not enough space to copy the file

**Symptoms:**
```
❌ Could not move file: [Errno 28] No space left on device
```

**Solution:**
- Free up disk space
- Check: Apple menu → About This Mac → Storage

### 4. Permission Denied (Rare)

**Problem:** Don't have write access to destination

**Symptoms:**
```
❌ Permission denied: Cannot create folder /path/to/folder
```

**Solution:**
```bash
# Check permissions
ls -la "/Users/chadmiller/Documents/Filing Cabinet"

# Fix if needed (shouldn't be necessary)
chmod u+w "/Users/chadmiller/Documents/Filing Cabinet"
```

### 5. File Already Exists

**Not an error** - Tool handles this automatically:
```
⚠️  File already exists at destination
📝 Using unique name: App Store_2025-01-15_2025_1.pdf
```

The tool adds a number to make the filename unique.

## Error Handling in the Tool

The tool now includes comprehensive error handling:

### Permission Errors
```python
try:
    shutil.move(source, destination)
except PermissionError:
    print("❌ Permission denied")
    # Skips file, continues processing others
```

### OS Errors (file busy, disk full, etc.)
```python
except OSError as e:
    print("❌ Could not move file")
    print("💡 File might be open or disk might be full")
    # Skips file, continues processing others
```

### Unexpected Errors
```python
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    # Skips file, continues processing others
```

## What Happens on Error

1. **Error is displayed** with helpful message
2. **File is skipped** (left in Incoming Scans)
3. **Tool continues** processing other files
4. **On next run**, it will try again

This means **errors are non-fatal** - the tool won't crash, just skip problematic files.

## Testing Permissions

### Test Write Access to Filing Cabinet
```bash
touch "/Users/chadmiller/Documents/Filing Cabinet/test.txt"
```

If this works, you have write access.

Remove the test file:
```bash
rm "/Users/chadmiller/Documents/Filing Cabinet/test.txt"
```

### Test Folder Creation
```bash
mkdir -p "/Users/chadmiller/Documents/Filing Cabinet/2025/Test"
```

If this works, you can create subdirectories.

Remove the test folder:
```bash
rmdir "/Users/chadmiller/Documents/Filing Cabinet/2025/Test"
```

## macOS-Specific Considerations

### Full Disk Access (macOS 10.14+)

Some folders require "Full Disk Access" permission. Your folders **don't require this** because:
- ✅ Both are in your user directory
- ✅ Not system folders
- ✅ Not protected locations

If you ever got a permission error, you could grant Full Disk Access:
1. System Settings → Privacy & Security → Full Disk Access
2. Click the + button
3. Add Terminal (or whatever app runs the script)

**But this shouldn't be necessary for your setup.**

### iCloud Drive Permissions

iCloud Drive folders are **local folders that sync** to iCloud. They have the same permissions as any other folder in your home directory.

No special permissions needed.

## Dry Run Mode is Always Safe

Dry run mode (`--dry-run` or `dry-run` argument) **never modifies files**:
- ❌ Doesn't create folders
- ❌ Doesn't move files
- ❌ Doesn't rename files
- ✅ Only reads and reports

**Always safe to use**, regardless of permissions.

## Best Practices

### 1. Start with Dry Run
```bash
./run_incoming_scans.sh dry-run
```
This shows what would happen without actually doing it.

### 2. Test with a Few Files
Put 1-2 test PDFs in Incoming Scans and run:
```bash
./run_incoming_scans.sh once
```

### 3. Check the Results
Verify files ended up in the right place in Filing Cabinet.

### 4. Then Use Watch Mode
Once confident:
```bash
./run_incoming_scans.sh watch
```

## Troubleshooting Commands

### Check who owns the folders:
```bash
ls -ld ~/Documents/Filing\ Cabinet
ls -ld ~/Library/Mobile\ Documents/com~apple~CloudDocs/Incoming\ Scans
```

Should show: `drwx------  ... chadmiller  staff  ...`

### Check if you can write:
```bash
[ -w ~/Documents/Filing\ Cabinet ] && echo "✅ Writable" || echo "❌ Not writable"
```

### Check folder permissions:
```bash
stat -f "%A %N" ~/Documents/Filing\ Cabinet
```

Typical output: `755` or `700` (both are fine)

## Summary

**For your setup:**
- ✅ Both folders in your home directory → Full permissions
- ✅ Error handling in place → Tool won't crash
- ✅ Dry run available → Test safely first
- ✅ Errors are skipped → Processing continues
- ✅ No sudo needed → Runs as regular user

**You should not have any permission problems.**

If you do encounter an issue:
1. Check the error message
2. See if file is open elsewhere
3. Try dry-run mode first
4. Check disk space

The tool is designed to be **fail-safe** - errors are handled gracefully and won't corrupt or lose your files.
