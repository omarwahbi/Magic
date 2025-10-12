# Item Code Enhancement Update

## What Changed

Added support for extracting and displaying **item codes** (4-7 digit codes) alongside national codes throughout the application.

## Understanding the Data Structure

### National Code vs Item Code

- **National Code**: Format `XX-XXX-XXX` (e.g., `04-A00-021`)
  - Spans columns 9 and 10 in PDF (both doubled)
  - Example: Col 9=`0044`, Col 10=`--AA0000--002211` → Fixed: `04-A00-021`

- **Item Code**: Format `4-7 digits` (e.g., `6549`, `418352`, `11071`)
  - Found in column 10 in PDF (NOT doubled - use raw value)
  - Each national code can have MULTIPLE items with different item codes

### PDF Structure Example

```
Row 1: National Code Row
  Col 9: 04
  Col 10: -A00-021
  Col 8: azepam 5mg
  → National Code: 04-A00-021

Row 2: Item Row (under national code 04-A00-021)
  Col 10: 6549          ← Item Code
  Col 8: Valium 5mgtab  ← Item Name
  Col 0: 31/08/2026     ← Expiry Date
  Col 7: 39.0           ← Balance

Row 3: Another Item Row (same national code)
  Col 10: 418352        ← Different Item Code
  Col 8: Valium 5mg     ← Different Item Name
  Col 0: 30/04/2028     ← Different Expiry
  Col 7: 30.0           ← Balance

Row 5: New National Code Row
  Col 9: 04
  Col 10: -A00-013
  → National Code: 04-A00-013

Row 6: Item Row
  Col 10: 11071
  ...
```

## Changes Made

### 1. Data Models (`src/models/extraction_data.py`)

**ExtractionData:**
- Added `item_codes: Dict[str, str]` - maps national_code → item_code
- Added `item_names: Dict[str, str]` - maps national_code → item_name
- Updated `expired_items`: Now `(national_code, item_code, name, expiry_date)`
- Updated `duplicates`: Now `(national_code, item_code, name)` for ALL occurrences

**ExtractionResult:**
- Updated `unmatched_codes`: Now `(national_code, item_code, name, balance)`
- Updated `expired_items`: Now `(national_code, item_code, name, expiry_date)`
- Updated `duplicates`: Now `(national_code, item_code, name)`

### 2. PDF Extractor (`src/services/pdf_extractor.py`)

**New Method:**
```python
_extract_national_and_item_code(row) -> (national_code, item_code, is_national_code_row)
```
- Identifies if row contains national code or item code
- Handles doubled characters for national codes
- Uses raw values for item codes (not doubled)

**Updated Logic:**
- `_find_codes_in_table`: Now tracks ALL items under each national code
- Detects duplicates when one national code has multiple items
- Records each item with its item code and name

**Updated Methods:**
- `_is_item_expired`: Now accepts national_code + item_code
- `_extract_balance`: Now accepts national_code + item_code + name
- Expiry date read from column 0 of item row
- Balance read from configured column of item row

### 3. Data Validator (`src/services/data_validator.py`)

- Updated `validate_and_match`: Includes item_code and name in unmatched codes

### 4. Export Service (`src/services/export_service.py`)

**Updated Exports:**
- `export_unmatched_codes`: Columns: National Code, Item Code, Item Name, Balance
- `export_expired_items`: Columns: National Code, Item Code, Item Name, Expiry Date
- `export_duplicates`: Columns: National Code, Item Code, Item Name

### 5. UI Components

**Results Tabs (`src/ui/components/results_tabs.py`):**
- Unmatched codes tree now shows: National Code | Item Code | Item Name | Balance

**Issues Tabs (`src/ui/components/issues_tabs.py`):**
- Expired items tree: National Code | Item Code | Item Name | Expiry Date
- Duplicates tree: National Code | Item Code | Item Name (shows ALL items for duplicated national codes)

## Reports Now Show

### 1. Unmatched Codes Report
Codes found in PDF but NOT in Excel:
- National Code (e.g., `04-A00-021`)
- Item Code (e.g., `6549`)
- Item Name (e.g., `Valium 5mgtab`)
- Balance

### 2. Expired Items Report
Items that were skipped because they're expired:
- National Code
- Item Code
- Item Name
- Expiry Date

### 3. Duplicate Codes Report
When ONE national code has MULTIPLE items (different manufacturers):
- Shows ALL items with that national code
- Each row: National Code | Item Code | Item Name
- Example: If `04-A00-021` has 2 items, shows 2 rows with same national code but different item codes and names

## Key Features

✅ **Preserves Balance Extraction Logic**: Didn't touch the core balance extraction
✅ **Handles Multiple Items per National Code**: Correctly identifies when 1 national code = multiple items
✅ **Proper Duplicate Detection**: Duplicate = national code appearing with multiple items
✅ **Complete Information**: All reports show national code + item code + item name
✅ **Correct Column Identification**: Distinguishes between national code rows and item rows

## Example Output

### Duplicate Report:
```
National Code | Item Code | Item Name
04-A00-021    | 6549      | Valium 5mgtab
04-A00-021    | 418352    | Valium 5mg
```
This shows that national code `04-A00-021` has 2 different items from different manufacturers.

### Expired Report:
```
National Code | Item Code | Item Name     | Expiry Date
04-A00-021    | 6549      | Valium 5mgtab | 31/08/2026
```

### Unmatched Report:
```
National Code | Item Code | Item Name   | Balance
05-B00-123    | 7890      | Medicine X  | 50.0
```

## Testing

To test, run the application with your PDF:
```bash
cd C:\Users\Omar\Desktop\magic
python run_app.py
```

1. Select PDF: `G:\My Drive\magic\pdfs\حسب الرمز الوطني\الموثرات.pdf`
2. Select Excel file
3. Choose "Stock" type
4. Click "Extract from PDF(s)"
5. Check all three reports to see national codes + item codes + names

## Logs

Enable DEBUG logging to see extraction details:
- Edit `src/config/settings.py`
- Change `level: int = logging.DEBUG`
- Check `extraction_log.txt` after extraction

You'll see logs like:
```
Found national code row: 04-A00-021
Found item code: 6549
Item 6549 under national code 04-A00-021, name: Valium 5mgtab
National code 04-A00-021 has 2 items (duplicate)
```

## Summary

The application now correctly:
1. Identifies national codes (XX-XXX-XXX format spanning 2 columns)
2. Identifies item codes (4-7 digits in single column)
3. Associates multiple items with one national code
4. Shows complete information in all reports
5. Maintains all original functionality
