# Filing Cabinet Organization Structure

This document explains how PDFs from your "Incoming Scans" folder will be organized into your "Filing Cabinet" folder.

## Source and Destination

**Source (Watched):**
```
/Users/chadmiller/Library/Mobile Documents/com~apple~CloudDocs/Incoming Scans
```

**Destination (Organized):**
```
/Users/chadmiller/Documents/Filing Cabinet
```

## Folder Structure

PDFs are automatically organized by **year** and **category**:

```
Filing Cabinet/
├── 2023/
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
    ├── Banking/
    │   ├── Statements/
    │   └── Credit Cards/
    ├── Invoices/
    ├── Taxes/
    ├── Bills/
    │   └── Utilities/
    ├── Medical/
    └── Insurance/
```

## How Files Are Organized

### App Store Receipts
**Detected by:** "receipt" + "icloud" in PDF content
**Renamed to:** `App Store_2025-01-15_2025.pdf`
**Moved to:** `Filing Cabinet/2025/Receipts/`

### Bank Statements
**Detected by:** "statement" + "account" or "balance" in PDF
**Renamed to:** `Bank_Statement_2025-01-01.pdf`
**Moved to:** `Filing Cabinet/2025/Banking/Statements/`

### Credit Card Statements
**Detected by:** "credit card" or card brands (Visa, Mastercard, Amex)
**Renamed to:** `CC_Statement_2025-01-15.pdf`
**Moved to:** `Filing Cabinet/2025/Banking/Credit Cards/`

### Invoices
**Detected by:** "invoice" in PDF content
**Renamed to:** `Invoice_2025-01-10_2025.pdf`
**Moved to:** `Filing Cabinet/2025/Invoices/`

### Tax Documents
**Detected by:** "tax", "irs", "1099", or "w-2" in PDF
**Renamed to:** `Tax_2025_2025-04-15.pdf`
**Moved to:** `Filing Cabinet/2025/Taxes/`

### Utility Bills
**Detected by:** "bill" or "utility", "electric", "water", "gas", "internet"
**Renamed to:** `Utility_Bill_2025-01-05.pdf`
**Moved to:** `Filing Cabinet/2025/Bills/Utilities/`

### Medical Documents
**Detected by:** "patient", "medical", "eob", or "explanation of benefits"
**Renamed to:** `Medical_2025-01-20.pdf`
**Moved to:** `Filing Cabinet/2025/Medical/`

### Insurance Documents
**Detected by:** "insurance" or "policy" in PDF
**Renamed to:** `Insurance_2025-01-15.pdf`
**Moved to:** `Filing Cabinet/2025/Insurance/`

## Automatic Year Detection

**The year is automatically detected from the PDF content, NOT the filename!**

This means:
- ✅ A receipt scanned in 2026 but dated 2025 will go to `Filing Cabinet/2025/`
- ✅ Tax documents from 2024 will go to `Filing Cabinet/2024/` even if scanned later
- ✅ No need to update rules every year
- ✅ Works automatically for past, present, and future years

### Fallback Behavior
If no year is found in the PDF content:
- Uses the current year as default
- File still gets organized properly

## Example Workflow

1. **You scan** an App Store receipt dated January 15, 2025
2. **Scanner saves** it to: `Incoming Scans/IMG_1234.pdf`
3. **Tool reads** the PDF and finds "receipt" and "iCloud" keywords
4. **Tool extracts** date: "January 15, 2025" from the PDF content
5. **Tool renames** to: `App Store_2025-01-15_2025.pdf`
6. **Tool moves** to: `Filing Cabinet/2025/Receipts/App Store_2025-01-15_2025.pdf`
7. **iCloud syncs** the organized file across your devices

## Handling Duplicates

If a file with the same name already exists:
- Tool adds a number: `App Store_2025-01-15_2025_1.pdf`
- Original file is never overwritten
- You can manually merge/delete duplicates later

## Customizing Categories

Edit `pdf_rules_filing_cabinet.json` to:
- Add new categories
- Change keywords for detection
- Modify rename patterns
- Change folder destinations

### Example: Add Category for Subscription Receipts

Add this to `pdf_rules_filing_cabinet.json`:

```json
{
  "name": "Subscription Receipts",
  "description": "Monthly subscription payments",
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

## Benefits of Year-Based Organization

✅ **Easy browsing** - All 2025 documents in one place
✅ **Tax time** - Quickly grab all documents from a tax year
✅ **Archiving** - Easy to archive old years to external storage
✅ **Compliance** - Many records require 7-year retention - easy to track
✅ **Automatic** - Year detection from content, not manual organization

## Existing Folders

The tool will work with your existing Filing Cabinet structure:
- Creates new year folders as needed (e.g., `2025/`, `2026/`)
- Creates new category folders as needed
- Preserves any existing files
- Never deletes or modifies existing content

## Quick Reference

| Document Type | Keywords | Destination |
|---------------|----------|-------------|
| App Store Receipts | receipt, icloud | `{year}/Receipts/` |
| Bank Statements | statement, account, balance | `{year}/Banking/Statements/` |
| Credit Cards | credit card, visa, mastercard | `{year}/Banking/Credit Cards/` |
| Invoices | invoice | `{year}/Invoices/` |
| Tax Documents | tax, irs, 1099, w-2 | `{year}/Taxes/` |
| Utility Bills | bill, utility, electric, water | `{year}/Bills/Utilities/` |
| Medical | patient, medical, eob | `{year}/Medical/` |
| Insurance | insurance, policy | `{year}/Insurance/` |

---

**Note:** All paths use `{year}` as a placeholder that gets replaced with the actual year extracted from each PDF's content.
