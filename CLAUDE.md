# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Balance Updater** is a pharmaceutical balance extraction tool that extracts medicine balance data from PDF files and updates Excel spreadsheets. The application has been refactored from a monolithic 526-line file into a modular architecture with 24+ files following clean architecture principles.

**NOTE:** This codebase uses a modular clean architecture with 24+ files organized in the `src/` directory. The original monolithic version has been removed.

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
# Quick build
build.bat

# Or using Python
python build_executable.py

# Or manual PyInstaller
pip install pyinstaller
pyinstaller --name=Magic --onefile --windowed --add-data="src;src" --hidden-import=sv_ttk run_app.py
```

Output: `dist/Magic.exe` (works on any Windows PC without Python)

## Architecture Overview

### Clean Architecture Layers

```
src/
├── config/              # Configuration layer
│   ├── settings.py      # App-wide settings (file paths, defaults)
│   └── extraction_config.py  # PDF extraction type configurations
│
├── models/              # Data models (pure data structures)
│   ├── item.py          # Medicine item with expiry validation
│   └── extraction_data.py  # Extraction results, validation results
│
├── services/            # Business logic (NO UI dependencies)
│   ├── pdf_extractor.py    # PDF extraction logic
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
    ├── style.py            # UI styling configuration (sv-ttk based)
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

The PDF extraction has complex business logic for handling doubled characters in PDF text:

**Doubled Character Bug**: PDFPlumber sometimes extracts text with doubled characters (e.g., "HHeelllloo" instead of "Hello"). The `fix_doubled_chars()` utility handles this by taking every other character.

**National Code Pattern**: Medicine codes follow format `XX-XXX-XXX` (e.g., "IR-12B-001")
- Must be uppercase
- Validated using regex: `([A-Z0-9]{2}-[A-Z0-9]{3}-+[A-Z0-9]{3})`

**Extraction Types**: Three types with different column mappings:
- **Stock**: Column 7 (actual balance) → Excel Column G
- **Free**: Column 2 (incoming items) → Excel Column F
- **Buy**: Column 2 (purchases) → Excel Column H

Configuration is in `src/config/extraction_config.py` - modify there to change column mappings.

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

### UI Architecture & Styling

The modular UI uses `sv-ttk` (Sun Valley ttk theme) for modern styling:
- **Theme**: Sun Valley Light theme via `sv_ttk.set_theme("light")`
- **Color scheme**: Blue primary (#2196F3), green success (#4CAF50), orange warning (#FF9800), red danger (#F44336)
- **Centralized styles**: All styling defined in `src/ui/style.py` using `AppStyle` class
- **Styled components**: Custom button styles (Success, Primary, Warning), treeview, labels, notebook tabs
- **Fonts**: Arial-based with 10pt/12pt sizes, bold variants for headers
- **Tooltips**: Custom tooltip widget in `src/ui/widgets/tooltip.py`

See `src/ui/style.py:24` for the `configure_styles()` method that sets up all TTK styles.

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
- Styling: Modify `src/ui/style.py` for colors, fonts, button styles
- Keep UI logic separate from business logic

**UI Initialization Order (Critical):**
1. Create `tk.Tk()` root window
2. Call `sv_ttk.set_theme("light")` to apply theme
3. Call `AppStyle.configure_styles()` to apply custom styles
4. Create application window
See `src/main.py:28-33` for the correct initialization sequence.

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
2. Add missing imports: `--hidden-import=module_name` (especially `--hidden-import=sv_ttk`)
3. Clean build: Delete `build/` and `dist/` folders, rebuild
4. Use `build.bat` or `build_executable.py` for correct configuration

**Note**: Build scripts may reference "BalanceUpdater" but the current executable is named "Magic.exe". Update build scripts if you need the "BalanceUpdater" name.

## Configuration Files

### requirements.txt
Critical dependencies:
- `pdfplumber>=0.9.0` - PDF text extraction
- `pandas>=2.0.0` - Data manipulation
- `openpyxl>=3.1.0` - Excel file handling
- `sv-ttk>=2.5.5` - Sun Valley TTK theme for modern UI
- Standard library: `tkinter`, `logging`, `datetime`, `re`

### settings.json
User preferences stored here:
- Last selected extraction type
- Recent file paths (future feature)

Created at runtime if not exists. Location: project root.

## Build & Distribution

See detailed guides:
- `BUILD_INSTRUCTIONS.md` - Comprehensive build documentation
- `QUICK_BUILD_GUIDE.md` - Fast build steps
- `HOW_TO_DISTRIBUTE.md` - Distribution options

Quick build: Double-click `build.bat` or run `python build_executable.py`

## File Naming Conventions

- **Services**: `*_service.py` or `*_handler.py` (e.g., `export_service.py`, `excel_handler.py`)
- **Utils**: `*_utils.py` or descriptive name (e.g., `date_utils.py`, `text_cleaner.py`)
- **Components**: Descriptive name (e.g., `file_selector.py`, `results_tabs.py`)
- **Models**: Singular noun (e.g., `item.py`, `extraction_data.py`)

## Code Style Notes

- **Type hints**: Use throughout for IDE support
- **Docstrings**: All public methods must have docstrings
- **Error handling**: Services raise exceptions, UI catches and displays
- **Logging**: Use `logging.warning()` for issues, not `print()`
- **Constants**: UPPER_CASE in config files or at module top
- **UI strings**: Can be extracted to config for i18n (future)

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

## Future Enhancements (Architecture Ready For)

The modular architecture makes these easy to add:
1. **Database support**: Add repository layer in `services/`
2. **API integration**: Add API client in `services/`
3. **Async processing**: Refactor services to use `asyncio`
4. **Plugin system**: Services already injectable
5. **Multi-language**: Extract UI strings to config
6. **Batch processing**: Add batch service in `services/`
7. **CLI interface**: Create CLI entry point using same services
8. **Web interface**: Services are UI-agnostic

## Important Files to Understand

Must read when making changes:
1. `src/config/extraction_config.py` - Column mappings and extraction logic
2. `src/services/pdf_extractor.py` - Core PDF extraction (most complex)
3. `src/utils/text_cleaner.py` - Handles doubled character bug
4. `src/ui/main_window.py` - UI orchestration
5. `src/ui/style.py` - UI styling and theming configuration
6. `src/main.py` - Application entry point

## Version History

- **v1.0**: Original monolithic file (526 lines)
- **v2.0**: Refactored to modular architecture (24+ files)
- **v2.1**: Integrated sv-ttk theme library for modern UI styling
- **Current**: Fully modular architecture with clean separation of concerns
