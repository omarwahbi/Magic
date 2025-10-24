# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Magic** is a pharmaceutical balance extraction tool that extracts medicine balance data from PDF files and updates Excel spreadsheets. The application uses a modular clean architecture with organized layers for maintainability and extensibility.

## Running the Application

### Development
```bash
# Always run from project root
cd "C:\Users\Omar\Desktop\magic - refractored"
python run_app.py

# Alternative
python -m src.main
```

**CRITICAL:** Always run from the project root directory, NEVER from inside src/. Running from src/ will cause import errors.

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Building Standalone Executable
```bash
# Quick build (Windows)
build.bat

# Cross-platform build
python build_executable.py
```

Output: `dist/Magic.exe` (works on any Windows PC without Python)

For detailed build instructions, see `BUILD_GUIDE.md`.

## Architecture Overview

### Clean Architecture Layers

```
src/
├── config/              # Configuration layer
│   ├── settings.py      # App-wide settings (file paths, defaults, logging)
│   └── extraction_config.py  # PDF extraction type configurations
│
├── models/              # Data models (pure data structures)
│   ├── item.py          # Medicine item with expiry validation
│   └── extraction_data.py  # Extraction results, validation results
│
├── services/            # Business logic (NO UI dependencies)
│   ├── pdf_extractor.py    # PDF extraction logic with warnings
│   ├── excel_handler.py    # Excel read/write operations
│   ├── data_validator.py   # Data validation & matching
│   ├── export_service.py   # Export to Excel functionality
│   └── settings_manager.py # Settings persistence
│
├── utils/               # Utility functions (pure functions)
│   ├── text_cleaner.py     # fix_doubled_chars, text processing
│   ├── date_utils.py       # Date parsing & validation
│   └── regex_patterns.py   # Reusable regex patterns
│
└── ui/                  # User interface (presentation only)
    ├── main_window.py      # Main application window
    ├── theme.py            # Theme system (colors, icons, typography, spacing)
    ├── components/         # UI components
    │   ├── file_selector.py
    │   ├── type_selector.py
    │   ├── manual_entry.py
    │   ├── results_tabs.py
    │   └── issues_tabs.py
    └── widgets/            # Reusable widgets
        ├── data_tree.py
        ├── loading_dialog.py
        └── tooltip.py
```

### Key Design Principles

1. **Separation of Concerns**: UI, business logic, data, and config are completely separated
2. **Single Responsibility**: Each module has ONE clear purpose
3. **Dependency Injection**: Services don't know about UI
4. **No Circular Dependencies**: Clean unidirectional data flow
5. **Type Safety**: Type hints throughout for IDE support

## Critical Implementation Details

### PDF Extraction Logic

**Doubled Character Bug**: PDFPlumber sometimes extracts text with doubled characters (e.g., "HHeelllloo" instead of "Hello"). The `fix_doubled_chars()` utility handles this by taking every other character.

**National Code Pattern**: Medicine codes follow format `XX-XXX-XXX` (e.g., "02-K00-002")
- Must be uppercase
- Validated using regex: `([A-Z0-9]{2}-[A-Z0-9]{3}-+[A-Z0-9]{3})`

**Extraction Types**: Three types with different column mappings:
- **Stock**: Column 7 (actual balance) → Excel Column G
- **Free**: Column 2 (incoming items) → Excel Column F
- **Buy**: Column 2 (purchases) → Excel Column H

Configuration is in `src/config/extraction_config.py` - modify there to change column mappings.

### Warnings System

The extraction process logs warnings to `extraction_log.txt`:

1. **Cross-Page Continuation** (INFO level):
   - Items at page start without national code header
   - Assigned to previous page's national code
   - May indicate missing headers in PDF
   - Format: `ℹ️ Cross-page continuation in '{filename}': Item {code} ('{name}') assigned to national code {nc} from previous page/table`

2. **Orphan Items** (WARNING level):
   - Items with NO national code at all
   - Will be skipped during extraction
   - Format: `⚠️ ORPHAN ITEM in '{filename}' at row {row}: Item code '{code}', name '{name}' has NO national code header!`

Logging configuration in `src/config/settings.py` - currently set to INFO level to capture all warnings.

### Expiry Date Validation

Items with expired dates are automatically skipped during extraction:
- Date format: DD/MM/YYYY
- Comparison: If year < current OR (same year AND month < current)
- Expired items are collected and shown in "Data Issues" → "Expired Items" tab

### Data Flow

```
User selects files
    ↓
PDFExtractor.extract_from_files()
    → Reads PDFs
    → Cleans text with fix_doubled_chars()
    → Extracts national codes + balances
    → Logs cross-page continuation warnings
    → Validates expiry dates
    → Returns ExtractionData
    ↓
DataValidator.validate_and_match()
    → Compares with Excel codes
    → Identifies: matched, unmatched, duplicates
    → Returns ExtractionResult
    ↓
UI displays results in tabs
    ↓
ExcelHandler.update_and_save()
    → Writes to correct column based on type
    → Saves with timestamp
```

### UI Architecture & Modern Design System

The modular UI uses a custom theme system for modern, professional appearance:

**Theme System** (`src/ui/theme.py`):
- **Colors**: Indigo primary (#6366F1), Emerald success (#10B981), Amber warning (#F59E0B), Red error (#EF4444)
- **Typography**: Segoe UI font family, multiple size scales (11-24pt)
- **Spacing**: 8px grid system (xs=4px, sm=8px, md=16px, lg=24px, xl=32px, xxl=48px)
- **Icons**: Unicode emoji icons for consistent visual indicators (✨📊✓⚠️🔍📕📗)
- **Components**: Pre-defined button, card, and status badge styles

**Layout** (`src/ui/main_window.py`):
- Card-based design for visual hierarchy
- Horizontal layouts for better flow
- Fixed button widths (no awkward expanding)
- Enhanced status bar with border and padding
- Three-section structure: Top (inputs), Middle (results), Bottom (actions)

**Key Features**:
- View Log button (🔍 View Log) - Opens extraction_log.txt in default editor
- Icons throughout UI for visual feedback
- Modern button sizing (Extract=20, Export=15, Save=30, View Log=15)
- Status messages with contextual icons

### Common Development Patterns

**Adding a New Extraction Type:**
1. Add entry to `ExtractionConfig.MAPPINGS` in `src/config/extraction_config.py`
2. Add radio button in `src/ui/components/type_selector.py`
3. Done! No other changes needed.

**Adding New Validation:**
1. Add method to `DataValidator` in `src/services/data_validator.py`
2. Call from `validate_and_match()` or create new service method
3. Update UI to display results

**Modifying UI:**
- Main window layout: `src/ui/main_window.py`
- Individual components: `src/ui/components/*.py`
- Reusable widgets: `src/ui/widgets/*.py`
- Theme (colors, icons, spacing): `src/ui/theme.py`
- Keep UI logic separate from business logic

**Using Theme System:**
```python
from src.ui.theme import theme, icons

# Colors
primary_color = theme.colors.primary  # #6366F1
success_color = theme.colors.success  # #10B981

# Spacing
padding = theme.spacing.md  # 16px
margin = theme.spacing.sm   # 8px

# Icons
button_text = f"{icons.MAGIC} Extract Data"  # ✨ Extract Data
status_text = f"{icons.SUCCESS} Complete"     # ✓ Complete
```

## Testing Strategy

Services are designed to be testable without UI:

```python
# Example unit tests
from src.services.pdf_extractor import PDFExtractor
from src.config.extraction_config import ExtractionType

def test_extraction():
    extractor = PDFExtractor(ExtractionType.STOCK)
    result = extractor.extract_from_files(['test.pdf'])
    assert 'XX-XXX-XXX' in result.balances

def test_text_cleaning():
    from src.utils.text_cleaner import fix_doubled_chars
    assert fix_doubled_chars("HHeelllloo") == "Hello"
```

Run tests (when implemented):
```bash
pytest tests/
```

## Common Issues & Solutions

### Import Errors
**Error**: `ImportError: attempted relative import beyond top-level package`
**Solution**: You're running from inside `src/`. Always run from project root using `python run_app.py`

### Module Not Found
**Error**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Change directory to project root: `cd "C:\Users\Omar\Desktop\magic - refractored"`

### Loading Dialog Issues
The loading dialog displays during PDF extraction. If it appears blank, ensure:
- `LoadingDialog` has both label and progressbar
- Window is properly centered using `transient()` and `grab_set()`
- `update()` is called on the loading window during processing

### Building Executable Fails
If PyInstaller build fails:
1. Ensure all dependencies installed: `pip install -r requirements.txt`
2. Add missing imports: `--hidden-import=module_name`
3. Clean build: Delete `build/` and `dist/` folders, rebuild
4. Use `build.bat` or `build_executable.py` for correct configuration

See `BUILD_GUIDE.md` for detailed troubleshooting.

## Configuration Files

### requirements.txt
Critical dependencies:
- `pdfplumber>=0.9.0` - PDF text extraction
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel file handling
- Standard library: `tkinter`, `logging`, `datetime`, `re`

### settings.json
User preferences stored here:
- Excel file path (persisted between sessions)
- Created at runtime if not exists
- Location: project root

### extraction_log.txt
Extraction warnings and diagnostic information:
- Cross-page continuation warnings
- Orphan item warnings
- Duplicate code warnings
- Saved extraction statistics
- Location: project root
- Level: INFO (configured in `src/config/settings.py`)

## Documentation Structure

```
magic/
├── README.md              # Project overview and quick start
├── USER_GUIDE.md          # Complete user manual
├── BUILD_GUIDE.md         # Build and distribution guide
├── TROUBLESHOOTING.md     # Common issues and solutions
└── CLAUDE.md             # This file - AI context
```

All documentation consolidated into 5 essential files. Old documentation removed for clarity.

## File Naming Conventions

- **Services**: `*_service.py` or `*_handler.py` (e.g., `export_service.py`, `excel_handler.py`)
- **Utils**: `*_utils.py` or descriptive name (e.g., `date_utils.py`, `text_cleaner.py`)
- **Components**: Descriptive name (e.g., `file_selector.py`, `results_tabs.py`)
- **Models**: Singular noun (e.g., `item.py`, `extraction_data.py`)

## Code Style Notes

- **Type hints**: Use throughout for IDE support
- **Docstrings**: All public methods must have docstrings
- **Error handling**: Services raise exceptions, UI catches and displays
- **Logging**: Use `logging.info()` / `logging.warning()` for diagnostic messages
- **Constants**: UPPER_CASE in config files or at module top
- **Icons**: Use `icons` from theme.py for consistency

## Performance Considerations

- **Large PDFs**: Extraction can take 30+ seconds for multi-page PDFs
- **Loading dialog**: Always show during long operations
- **Memory**: PDFPlumber keeps pages in memory - process page by page
- **Excel updates**: Use openpyxl's optimized mode for large files

## Security Notes

- **No sensitive data**: Application doesn't store credentials
- **File paths only**: Settings store paths, not file contents
- **Local processing**: All data processing happens locally
- **No network calls**: Application is fully offline

## Important Files to Understand

Must read when making changes:
1. `src/config/extraction_config.py` - Column mappings and extraction logic
2. `src/services/pdf_extractor.py` - Core PDF extraction with warnings (most complex)
3. `src/utils/text_cleaner.py` - Handles doubled character bug
4. `src/ui/main_window.py` - UI orchestration and layout
5. `src/ui/theme.py` - Theme system (colors, icons, spacing, typography)
6. `src/config/settings.py` - App settings and logging configuration

## Version History

- **v1.0**: Original monolithic file (526 lines)
- **v2.0**: Refactored to modular architecture (24+ files)
- **v2.1**: Added warnings system for cross-page continuation and orphan items
- **v2.2**: UI modernization with theme system, icons, and card-based layout
- **v2.3**: Documentation cleanup - consolidated into 5 essential files
- **Current**: Fully modular with clean architecture, modern UI, and comprehensive warnings

## Quick Reference

**User Documentation**: See `USER_GUIDE.md`
**Build Documentation**: See `BUILD_GUIDE.md`
**Troubleshooting**: See `TROUBLESHOOTING.md`
**Project Info**: See `README.md`
