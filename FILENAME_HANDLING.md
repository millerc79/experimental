# Filename Handling Guide

This guide explains how the PDF automation tool handles filename generation and sanitization.

## Filename Generation Process

### 1. Pattern Replacement

The tool uses patterns like:
```
App Store_{date}_{year}{ext}
```

Placeholders are replaced with actual values:
- `{date}` → Date from PDF content (e.g., `2025-01-15`)
- `{year}` → Year from PDF content (e.g., `2025`)
- `{ext}` → File extension (e.g., `.pdf`)
- `{date_created}` → File creation date (e.g., `2025-01-15`)
- `{original_name}` → Original filename without extension

**Example:**
```
Pattern:  "App Store_{date}_{year}{ext}"
Result:   "App Store_2025-01-15_2025.pdf"
```

### 2. Filename Sanitization

After generating the filename, it's automatically sanitized to ensure compatibility with both macOS and Windows filesystems.

## Filename Safety Rules

### Invalid Characters Removed

The following characters are **not allowed** in filenames and are replaced with `_`:

| Character | Why Invalid | Replacement |
|-----------|-------------|-------------|
| `/` | macOS/Windows path separator | `_` |
| `\` | Windows path separator | `_` |
| `:` | macOS special, Windows drive separator | `_` |
| `*` | Windows wildcard | `_` |
| `?` | Windows wildcard | `_` |
| `"` | Windows reserved | `_` |
| `<` | Windows reserved | `_` |
| `>` | Windows reserved | `_` |
| `|` | Windows pipe operator | `_` |

**Example:**
```
Before: "Statement: Jan/Feb 2025.pdf"
After:  "Statement_ Jan_Feb 2025.pdf"
```

### Multiple Underscores Collapsed

Multiple consecutive underscores are reduced to a single underscore:

```
Before: "App___Store____Receipt.pdf"
After:  "App_Store_Receipt.pdf"
```

### Leading/Trailing Characters Trimmed

Spaces and periods at the start or end are removed:

```
Before: "  Receipt .pdf"
After:  "Receipt.pdf"
```

### Control Characters Removed

Invisible Unicode control characters (like newlines, tabs) are removed:

```
Before: "Receipt\n\t2025.pdf"
After:  "Receipt2025.pdf"
```

### Reserved Names Handled (Windows)

Windows reserves certain names that can't be used as filenames:
- `CON`, `PRN`, `AUX`, `NUL`
- `COM1` through `COM9`
- `LPT1` through `LPT9`

If a generated name matches one of these, it's prefixed with an underscore:

```
Before: "CON.pdf"
After:  "_CON.pdf"
```

### Empty Names

If sanitization removes all characters, the name becomes:

```
"unnamed.pdf"
```

## Length Limits

### Maximum Length: 255 Bytes

macOS and most modern filesystems have a 255-byte limit for filenames (not characters, **bytes** - important for Unicode).

### Automatic Truncation

If a generated filename exceeds 255 bytes:

1. The extension is preserved (`.pdf`)
2. The name is truncated to fit
3. A 10-byte buffer is left for safety

**Example:**
```
Pattern produces a very long name:
"Bank_Statement_for_Account_123456789_with_transactions_and_balances_2025-01-15_2025.pdf"

If too long, automatically truncated to:
"Bank_Statement_for_Account_123456789_with_transactions_and_balan_2025.pdf"
```

### UTF-8 Considerations

Some characters use multiple bytes in UTF-8:
- `A` = 1 byte
- `é` = 2 bytes
- `日` = 3 bytes

The tool counts **bytes**, not characters, to ensure compatibility.

## Real-World Examples

### Example 1: App Store Receipt

**PDF Content:** Receipt dated "January 15, 2025" with text "iCloud Storage"

**Rule Pattern:** `App Store_{date}_{year}{ext}`

**Generated:** `App Store_2025-01-15_2025.pdf`

**Sanitized:** `App Store_2025-01-15_2025.pdf` ✅ (no changes needed)

### Example 2: Bank Statement with Special Characters

**PDF Content:** Statement dated "12/31/2024" with account "Account #12345"

**Rule Pattern:** `Bank_{original_name}_{date}{ext}`

**Original Name:** `Statement: 12/31/2024.pdf`

**Generated:** `Bank_Statement: 12/31/2024_2024-12-31.pdf`

**Sanitized:** `Bank_Statement_ 12_31_2024_2024-12-31.pdf` ✅

Changes made:
- `:` → `_`
- `/` → `_`

### Example 3: Reserved Windows Name

**PDF Content:** Document titled "CON"

**Rule Pattern:** `{original_name}_{year}{ext}`

**Generated:** `CON_2025.pdf`

**Sanitized:** `_CON_2025.pdf` ✅

Prefixed with `_` to avoid Windows reserved name.

### Example 4: Very Long Filename

**PDF Content:** Detailed invoice with long description

**Rule Pattern:** `Invoice_{original_name}_{date}{ext}`

**Original Name:** `Detailed_Monthly_Service_Invoice_for_Professional_Services_Rendered_Including_Consulting_Analysis_and_Implementation.pdf`

**Generated:** (over 255 bytes)

**Sanitized:** `Invoice_Detailed_Monthly_Service_Invoice_for_Professional_Services_Rendered_Including_Cons_2025-01-15.pdf` ✅

Automatically truncated to fit 255 bytes.

## Cross-Platform Compatibility

### macOS ✅
- Sanitizes `:` and `/`
- Handles 255-byte limit
- Removes leading/trailing dots

### Windows ✅
- Sanitizes all Windows-invalid characters
- Handles reserved names
- Works with 255-byte limit

### Linux ✅
- More permissive than macOS/Windows
- Sanitization ensures compatibility
- Works with 255-byte limit

## What Happens with Duplicates

After sanitization, if a file with the same name already exists, the tool adds a number:

```
First file:  App Store_2025-01-15_2025.pdf
Duplicate:   App Store_2025-01-15_2025_1.pdf
Another:     App Store_2025-01-15_2025_2.pdf
```

This happens **after** sanitization, so you won't lose files due to naming conflicts.

## Testing Filename Sanitization

Want to see how a filename would be sanitized? You can test it:

```python
from pdf_automation import sanitize_filename

# Test various problematic names
print(sanitize_filename("File:Name.pdf"))
# Output: File_Name.pdf

print(sanitize_filename("CON.pdf"))
# Output: _CON.pdf

print(sanitize_filename("File///Name.pdf"))
# Output: File_Name.pdf

print(sanitize_filename("  .Leading dots.pdf"))
# Output: Leading dots.pdf
```

## Edge Cases Handled

### Unicode Characters ✅
```
"Receipt_日本語_2025.pdf" → "Receipt_日本語_2025.pdf"
(Unicode is preserved if valid)
```

### Emoji ✅
```
"Receipt_📄_2025.pdf" → "Receipt_📄_2025.pdf"
(Emoji are preserved)
```

### Mixed Invalid Characters ✅
```
"File:/\*?.pdf" → "File____.pdf"
```

### All Invalid Characters ✅
```
":::/\\.pdf" → "unnamed.pdf"
```

### Extension Only ✅
```
".pdf" → "unnamed.pdf"
```

## Best Practices for Rename Patterns

### ✅ Good Patterns

```json
"rename_pattern": "Receipt_{date}_{year}{ext}"
"rename_pattern": "Bank_Statement_{year}-{date}{ext}"
"rename_pattern": "{year}_Tax_Document{ext}"
```

These produce clean, safe filenames.

### ⚠️ Patterns to Avoid

Avoid patterns that might produce very long names:

```json
"rename_pattern": "{original_name}_backup_copy_processed_{date}_{year}{ext}"
```

If `{original_name}` is already long, this could exceed 255 bytes.

Better:
```json
"rename_pattern": "{year}_{date}_{original_name}{ext}"
```

This way, the date comes first and original name gets truncated if needed.

## Troubleshooting

### Problem: Filenames Look Wrong

**Check:**
1. Look at the pattern in your rules file
2. Verify the PDF content contains the expected text
3. Run in dry-run mode to see before sanitization

### Problem: Files Not Found After Processing

**Possible Cause:** Filename was sanitized differently than expected

**Solution:**
1. Run dry-run mode first to see final names
2. Check the Filing Cabinet folders - files might have slightly different names
3. Look for files with `_` instead of special characters

### Problem: "File Already Exists" Warnings

**This is normal** when:
- You process the same PDFs multiple times
- Two PDFs have identical dates and match the same rule

**Tool behavior:**
- Adds number suffix: `_1`, `_2`, etc.
- Original file is preserved

## Summary

The tool's filename sanitization ensures:

✅ **Cross-platform compatibility** - Works on macOS, Windows, Linux
✅ **No crashes** - Invalid characters are handled gracefully
✅ **No data loss** - Files aren't skipped due to naming issues
✅ **Readable names** - Sanitization is minimal and sensible
✅ **Length limits respected** - Auto-truncates long filenames
✅ **Duplicates handled** - Adds numbers when needed

You don't need to worry about filename issues - the tool handles everything automatically!
