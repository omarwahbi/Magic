# Magic - User Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [How to Use the Application](#how-to-use-the-application)
3. [Understanding Results](#understanding-results)
4. [Viewing Warnings](#viewing-warnings)
5. [Export Options](#export-options)
6. [Manual Entry](#manual-entry)
7. [Common Issues](#common-issues)

---

## Quick Start

### Running the Application

**From Source:**
```bash
python run_app.py
```

**From Executable:**
- Double-click `Magic.exe` in the `dist` folder

---

## How to Use the Application

### Step 1: Select PDF Files
1. Click **"Browse PDFs"** button
2. Select one or more PDF files containing medicine balance data
3. Selected files will be shown in the interface

### Step 2: Set Default Excel File
1. In the **"Default Excel File"** section, click **"Change..."**
2. Select your master Excel file containing medicine codes
3. This file will be remembered for future sessions

### Step 3: Select Extraction Type
Choose the appropriate type based on your PDF format:

- **Stock**: Use for stock balance reports (column 7 balance → Excel Column G)
- **Free**: Use for free/incoming items (column 2 balance → Excel Column F)
- **Buy**: Use for purchase orders (column 2 balance → Excel Column H)

### Step 4: Extract Data
1. Click **✨ Extract Data** button
2. Wait for processing (progress dialog will show)
3. Results will appear in the tabs below

### Step 5: Review Results
Check the **"Extraction Results"** tabs:
- **Matched**: Items found in both PDF and Excel
- **Missing in PDF**: Excel codes not found in PDFs
- **Not in Excel**: PDF codes not found in Excel (unmatched)

Check the **"Data Issues"** tabs:
- **Expired Items**: Items with expired dates (automatically skipped)
- **Duplicates**: Codes appearing multiple times
- **Zero Balance**: Items with zero balance

### Step 6: Save Updated Excel
1. Review the matched items
2. Click **✓ Save Updated Excel** button
3. File will be saved with timestamp: `updated_medicines_YYYYMMDD_HHMMSS.xlsx`

---

## Understanding Results

### Matched Items
Items successfully found in both PDF and Excel:
- **National Code**: XX-XXX-XXX format (e.g., 02-K00-002)
- **Medicine Name**: From Excel file
- **Balance**: Extracted from PDF
- **Status**: "Matched"

### Missing in PDF
Excel codes that weren't found in the PDFs:
- Indicates medicines in your Excel that have no data in PDFs
- Check if PDFs are complete or if items are discontinued

### Not in Excel (Unmatched)
PDF codes not found in your Excel file:
- New medicines that need to be added to Excel
- Possible typos in PDF national codes
- Export these to add to your master Excel

### Expired Items
Items with expiry dates in the past:
- **Automatically skipped** during extraction
- Listed in "Data Issues" → "Expired Items" tab
- Check these items for disposal/replacement

### Duplicates
National codes appearing multiple times:
- Usually indicates PDF formatting issues
- May need manual review
- Listed in "Data Issues" → "Duplicates" tab

### Zero Balance
Items with balance = 0:
- Not an error, just informational
- Listed in "Data Issues" → "Zero Balance" tab

---

## Viewing Warnings

### What Are Warnings?

The extraction process logs warnings about potential data quality issues:

1. **Cross-Page Continuation**
   - Items at the start of a page without a national code header
   - Assigned to the previous page's national code
   - May be correct or may indicate missing headers

2. **Orphan Items**
   - Items with NO national code at all
   - Will be skipped during extraction
   - Indicates serious PDF formatting issues

### How to View Warnings

**Method 1: View Log Button**
1. After extraction, click **🔍 View Log** button
2. Log file opens in Notepad (Windows) or default text editor
3. Search for:
   - `ℹ️ Cross-page continuation` - Info messages
   - `⚠️ ORPHAN ITEM` - Warning messages

**Method 2: Open Log Manually**
- File location: `extraction_log.txt` (same folder as app)
- Open with any text editor

### Understanding Warning Messages

**Cross-Page Continuation Example:**
```
2025-10-24 12:55:13,823 - INFO - ℹ️ Cross-page continuation in 'اقراص الشركة العامة اسكان.pdf':
Item 6709 ('MELOXICAM 7.5') assigned to national code 02-K00-002 from previous page/table
```

**What this means:**
- File: اقراص الشركة العامة اسكان.pdf
- Item 6709 (MELOXICAM 7.5) was found at the start of a page
- No national code header on that page
- Assigned to previous page's code: 02-K00-002

**Action:** Check if MELOXICAM belongs to 02-K00-002 or if the PDF is missing a header.

---

## Export Options

### Export Unmatched
Export codes found in PDFs but not in your Excel:
1. Click **⬇️ Export** → **Export Unmatched**
2. Choose save location
3. Excel file created with unmatched codes and balances
4. Use this to add new medicines to your master Excel

### Export Expired
Export items with expired dates:
1. Click **⬇️ Export** → **Export Expired**
2. Choose save location
3. Excel file created with expired items
4. Use for disposal/replacement planning

### Export Duplicates
Export duplicate national codes:
1. Click **⬇️ Export** → **Export Duplicates**
2. Choose save location
3. Excel file created with duplicate codes
4. Review for PDF data quality issues

### Export Zero Balance
Export items with zero balance:
1. Click **⬇️ Export** → **Export Zero Balance**
2. Choose save location
3. Excel file created with zero balance items
4. Use for inventory planning

---

## Manual Entry

### When to Use Manual Entry
- Correct a balance value before saving
- Override an extracted value
- Add missing data

### How to Use
1. In **"Extraction Results"** → **"Matched"** tab, select a row
2. In **"Manual Entry"** section at bottom, enter new balance
3. Click **"Update Selected"** button
4. Balance will be updated in the results
5. Click **"Save Updated Excel"** to save changes

---

## Common Issues

### Issue: "Please select at least one PDF file"
**Solution:** Click "Browse PDFs" and select PDF files before clicking Extract.

### Issue: "Please set the default Excel file in Settings"
**Solution:** Click "Change..." in the Default Excel File section and select your Excel file.

### Issue: No data extracted from PDF
**Possible causes:**
1. Wrong extraction type selected (try Stock/Free/Buy)
2. PDF has no national codes in XX-XXX-XXX format
3. PDF is scanned image (not searchable text)
4. PDF structure is incompatible

**Solution:** Open the PDF and verify:
- National codes are in format XX-XXX-XXX (e.g., 02-K00-002)
- Text is selectable (not an image)
- Tables are properly formatted

### Issue: Wrong balance values extracted
**Possible causes:**
1. Wrong extraction type selected
2. PDF has unusual table structure
3. Cross-page continuation issue (check warnings)

**Solution:**
1. Verify extraction type (Stock/Free/Buy)
2. Click "View Log" to check for warnings
3. Use Manual Entry to correct values
4. Review PDF structure

### Issue: Items marked as "Not in Excel"
**Possible causes:**
1. New medicines not yet in master Excel
2. Typo in PDF national code
3. Excel file is outdated

**Solution:**
1. Export unmatched items
2. Review codes manually
3. Add valid new codes to master Excel
4. Fix typos in PDF if possible

### Issue: Extraction log shows cross-page warnings
**What it means:**
- Items at page boundaries assigned to previous code
- May be correct (legitimate continuation) or incorrect (missing header)

**Solution:**
1. Review the warning messages in log file
2. Check if the medicine name matches the national code
3. If wrong, manually correct in results before saving
4. Consider fixing the PDF source if possible

### Issue: Can't open log file
**Solution:**
1. Ensure you've run an extraction first (log file is created during extraction)
2. Check that `extraction_log.txt` exists in the same folder as the app
3. Try opening manually with Notepad

---

## Tips for Best Results

1. **Use consistent extraction type**: Don't mix Stock/Free/Buy in one session
2. **Review warnings**: Always check log file after extraction
3. **Verify cross-page items**: Check warnings for items at page boundaries
4. **Export unmatched codes**: Review and add to master Excel for future
5. **Manual review**: Check a few matched items manually to verify accuracy
6. **Keep Excel updated**: Regularly add new medicines from unmatched exports
7. **PDF quality matters**: Clean, properly formatted PDFs = better extraction

---

## Need Help?

If you encounter issues not covered in this guide:
1. Check `TROUBLESHOOTING.md` for detailed error solutions
2. Review the log file (`extraction_log.txt`) for diagnostic information
3. Ensure your PDF follows the expected format (XX-XXX-XXX national codes)
