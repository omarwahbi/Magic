# Semi-Automated Balance Updater

A modular Python application for extracting pharmaceutical balance data from PDF files and updating Excel spreadsheets.

## Features

- **PDF Extraction**: Extract medicine balance data from PDF files with national codes
- **Excel Integration**: Automatically update Excel spreadsheets with extracted data
- **Data Validation**:
  - Detect expired items
  - Identify duplicate codes
  - Find unmatched codes
- **Manual Correction**: Manually edit balance values when needed
- **Export Capabilities**: Export issues (expired, duplicates, unmatched) to Excel

## Project Structure

```
magic/
├── src/
│   ├── main.py                    # Application entry point
│   ├── config/                    # Configuration modules
│   │   ├── settings.py            # App-wide settings
│   │   └── extraction_config.py   # Extraction type configurations
│   ├── models/                    # Data models
│   │   ├── extraction_data.py     # Extraction data structures
│   │   └── item.py                # Medicine item model
│   ├── services/                  # Business logic layer
│   │   ├── pdf_extractor.py       # PDF extraction service
│   │   ├── excel_handler.py       # Excel operations service
│   │   ├── data_validator.py      # Data validation service
│   │   └── export_service.py      # Export service
│   ├── utils/                     # Utility functions
│   │   ├── text_cleaner.py        # Text processing
│   │   ├── date_utils.py          # Date handling
│   │   └── regex_patterns.py      # Regex patterns
│   └── ui/                        # User interface
│       ├── main_window.py         # Main application window
│       ├── components/            # UI components
│       │   ├── file_selector.py
│       │   ├── type_selector.py
│       │   ├── results_tabs.py
│       │   ├── issues_tabs.py
│       │   └── manual_entry.py
│       └── widgets/               # Base widgets
│           ├── data_tree.py
│           └── loading_dialog.py
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd C:\Users\Omar\Desktop\magic
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python run_app.py
   ```

   Or alternatively:
   ```bash
   python -m src.main
   ```

   **Important:** Always run from the project root directory, not from inside `src/`

## Usage

1. **Select PDF files**: Click "Browse" next to "PDFs:" to select one or more PDF files
2. **Select Excel file**: Click "Browse" next to "Excel:" to select your Excel file
3. **Choose extraction type**: Select Stock, Free, or Buy based on your PDF type
4. **Extract data**: Click "Extract from PDF(s)" to process the files
5. **Review results**:
   - Check the "Extraction Results" tab for matched and unmatched items
   - Check the "Data Issues" tab for expired items and duplicates
6. **Manual corrections**: Select a row and enter a manual balance if needed
7. **Save**: Click "Save Updated Excel" to export the results

## Extraction Types

- **Stock**: Extracts actual balance from stock PDFs (Column G in Excel)
- **Free**: Extracts incoming free items (Column F in Excel)
- **Buy**: Extracts purchased items (Column H in Excel)

## Architecture

This application follows clean architecture principles with clear separation of concerns:

- **Config Layer**: Application settings and configuration
- **Models Layer**: Data structures and business entities
- **Services Layer**: Business logic (PDF extraction, Excel operations, validation)
- **Utils Layer**: Reusable utility functions
- **UI Layer**: User interface components (decoupled from business logic)

### Key Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: Services are injected where needed
3. **Separation of Concerns**: UI, business logic, and data are separated
4. **Modularity**: Easy to test, maintain, and extend
5. **Type Safety**: Type hints throughout for better IDE support

## Development

### Running Tests

```bash
# Unit tests (if implemented)
python -m pytest tests/
```

### Adding New Features

The modular structure makes it easy to extend:

- Add new extraction types: Modify `config/extraction_config.py`
- Add new validation rules: Extend `services/data_validator.py`
- Add new UI components: Create in `ui/components/`
- Add new utilities: Create in `utils/`

## License

Internal use only.

## Original File

The original monolithic file is preserved as `semi_auto_balance_gui.py` for reference.
