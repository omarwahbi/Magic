# How to View Extraction Warnings

## Warning System Added

The app now logs warnings about potential data quality issues during extraction. These warnings help you identify problematic PDFs.

## Where to Find Warnings

**Log File Location:**
- When running from source: `extraction_log.txt` (project root)
- When running Magic.exe: `extraction_log.txt` (same folder as Magic.exe)

## Types of Warnings

### 1. ℹ️ Cross-Page Continuation (INFO)
```
ℹ️ Cross-page continuation: Item 6709 ('MELOXICAM 7.5') at row 2 assigned to national code 02-K00-002 from previous page/table
```

**What it means:**
- An item was found at the start of a new page without its own national code header
- The app assigned it to the national code from the previous page
- **Action**: Check if the medicine name matches the national code
  - If names match (e.g., "Brufen" under "Ibuprofen"): ✓ Correct
  - If names don't match (e.g., "MELOXICAM" under "Mebeverine"): ✗ Wrong - bad PDF data

### 2. ⚠️ Orphan Item (WARNING)
```
⚠️ ORPHAN ITEM DETECTED at row 5: Item code '6709', name 'MELOXICAM 7.5' has NO national code header!
   This item appears without a XX-XXX-XXX national code and will be SKIPPED.
   Check PDF structure - this section may be missing its national code header.
```

**What it means:**
- An item was found but there's no national code (not even from previous pages)
- The item will be SKIPPED
- **Action**: Check PDF - this section is missing its national code header

## How to Check the Log

### Option 1: Open the log file
1. Navigate to the app folder (where Magic.exe is located)
2. Open `extraction_log.txt` with Notepad
3. Search for "Cross-page" or "ORPHAN"

### Option 2: View in extraction_log.txt after running
The log file is overwritten each time you run an extraction, so check it immediately after processing PDFs.

## Example: Identifying Bad Data

If you see:
```
ℹ️ Cross-page continuation: Item 6709 ('MELOXICAM 7.5') assigned to 02-K00-002
```

**Check:**
1. What is 02-K00-002? → Mebeverine hydrochloride 135mg
2. What is item 6709? → MELOXICAM 7.5
3. Are they the same medicine? → **NO!**
4. **Conclusion**: Bad PDF data - Meloxicam section missing national code header

**Fix**: Either get a corrected PDF or manually remove the wrong items from the results.

## Current Limitation

Warnings are currently only written to the log file, not shown in the GUI. You must manually open `extraction_log.txt` to view them.

## Future Enhancement

In a future version, we could add a "View Warnings" button in the GUI to show these messages directly in the application.
