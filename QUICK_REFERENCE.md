# Quick Reference Card

## 🚀 How to Run

```bash
cd C:\Users\Omar\Desktop\magic
python run_app.py
```

## 📁 Project Structure

```
src/
├── config/      → Settings (colors, column mappings, etc.)
├── models/      → Data classes (ExtractionData, MedicineItem)
├── services/    → Business logic
│   ├── pdf_extractor.py    → Extracts from PDFs
│   ├── excel_handler.py    → Reads/writes Excel
│   ├── data_validator.py   → Validates & matches data
│   └── export_service.py   → Exports issues
├── utils/       → Helper functions
│   ├── text_cleaner.py     → Text processing
│   ├── date_utils.py       → Date handling
│   └── regex_patterns.py   → Regex constants
└── ui/          → User interface
    ├── main_window.py      → Main app window
    ├── components/         → UI components
    └── widgets/            → Reusable widgets
```

## 🔧 Common Tasks

### Change PDF Column for Extraction Type
**File:** `src/config/extraction_config.py`
```python
MAPPINGS = {
    ExtractionType.STOCK: ColumnMapping(
        pdf_column=7,    # ← Change this
        excel_column=6
    ),
}
```

### Change Excel Target Column
**File:** `src/config/extraction_config.py`
```python
MAPPINGS = {
    ExtractionType.STOCK: ColumnMapping(
        pdf_column=7,
        excel_column=6   # ← Change this
    ),
}
```

### Change UI Colors
**File:** `src/config/settings.py`
```python
COLOR_SUCCESS: str = "#d4edda"    # ← Change colors
COLOR_MISSING: str = "#f8d7da"
COLOR_PRIMARY: str = "#2196F3"
```

### Add New Validation Rule
**File:** `src/services/data_validator.py`
```python
class DataValidator:
    @staticmethod
    def your_new_validation(data):
        # Add your logic here
        pass
```

### Add New Extraction Type
1. **Add enum:** `src/config/extraction_config.py`
```python
class ExtractionType(Enum):
    STOCK = "Stock"
    FREE = "Free"
    BUY = "Buy"
    NEW_TYPE = "NewType"  # ← Add here
```

2. **Add mapping:** Same file
```python
MAPPINGS = {
    # ... existing ...
    ExtractionType.NEW_TYPE: ColumnMapping(
        pdf_column=X,
        excel_column=Y
    ),
}
```

3. **Add radio button:** `src/ui/components/type_selector.py` (automatic!)

## 🧪 Testing

### Test Text Cleaning
```python
from src.utils.text_cleaner import fix_doubled_chars
result = fix_doubled_chars("HHeelllloo")
print(result)  # "Hello"
```

### Test Date Parsing
```python
from src.utils.date_utils import parse_expiry_date, is_expired
date = parse_expiry_date("Expiry: 15/06/2025")
print(date)  # (15, 6, 2025)
print(is_expired(15, 6, 2020))  # True
```

### Test PDF Extraction
```python
from src.services.pdf_extractor import PDFExtractor
from src.config.extraction_config import ExtractionType

extractor = PDFExtractor(ExtractionType.STOCK)
data = extractor.extract_from_files(['test.pdf'])
print(data.balances)
```

## 📊 Key Classes

| Class | Purpose | Location |
|-------|---------|----------|
| `PDFExtractor` | Extract from PDFs | `services/pdf_extractor.py` |
| `ExcelHandler` | Excel operations | `services/excel_handler.py` |
| `DataValidator` | Validate data | `services/data_validator.py` |
| `ExportService` | Export data | `services/export_service.py` |
| `BalanceUpdaterApp` | Main GUI | `ui/main_window.py` |
| `DataTreeView` | Reusable tree widget | `ui/widgets/data_tree.py` |
| `LoadingDialog` | Loading screen | `ui/widgets/loading_dialog.py` |

## 🐛 Debugging

### Enable Debug Logging
**File:** `src/config/settings.py`
```python
class LoggingConfig:
    level: int = logging.DEBUG  # ← Change from WARNING to DEBUG
```

### Check Extraction Log
```bash
cat extraction_log.txt
```

## 📦 Dependencies

```bash
# Install
pip install -r requirements.txt

# Update
pip install --upgrade pdfplumber openpyxl pandas

# List installed
pip list | findstr "pdfplumber openpyxl pandas"
```

## ⚡ Performance Tips

1. **Process fewer PDFs at once** - Better progress tracking
2. **Use specific extraction type** - Correct column mapping
3. **Close other applications** - More memory available
4. **Large PDFs?** - May take longer, be patient

## 🔒 Safety Features

- ✅ Original Excel file never modified
- ✅ Creates new timestamped file
- ✅ Logs all operations
- ✅ Error handling throughout
- ✅ Validation before saving

## 📝 File Naming

**Output Excel:** `updated_medicines_YYYYMMDD_HHMMSS.xlsx`
**Example:** `updated_medicines_20250108_143022.xlsx`

## 🎯 Workflow

1. Select PDFs → Select Excel → Choose Type → Extract
2. Review Results → Check Issues → Manual corrections (if needed)
3. Save → New Excel file created!

## 📚 Documentation Files

- `START_HERE.md` - Quick start
- `README.md` - Full documentation
- `TROUBLESHOOTING.md` - Fix issues
- `REFACTORING_SUMMARY.md` - What changed
- `BEFORE_AFTER_COMPARISON.md` - Code examples
- `VERIFICATION_CHECKLIST.md` - Features list

---

**Need help?** Check TROUBLESHOOTING.md
