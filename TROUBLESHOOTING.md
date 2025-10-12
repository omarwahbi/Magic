# Troubleshooting Guide

## How to Run the Application

### ✅ Recommended Method (From Project Root)
```bash
cd C:\Users\Omar\Desktop\magic
python run_app.py
```

### ✅ Alternative Method
```bash
cd C:\Users\Omar\Desktop\magic
python -m src.main
```

### ❌ Don't Run From src/ Directory
```bash
# This will cause import errors:
cd src
python main.py  # ❌ Don't do this
```

## Common Issues

### Issue 1: Import Errors
**Error:**
```
ImportError: attempted relative import beyond top-level package
```

**Solution:**
Always run from the project root (`C:\Users\Omar\Desktop\magic`), not from the `src/` directory.

**Correct:**
```bash
cd C:\Users\Omar\Desktop\magic
python run_app.py
```

### Issue 2: Module Not Found
**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
Make sure you're in the project root directory:
```bash
cd C:\Users\Omar\Desktop\magic
python run_app.py
```

### Issue 3: Missing Dependencies
**Error:**
```
ModuleNotFoundError: No module named 'pdfplumber'
```

**Solution:**
Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue 4: Blank Loading Dialog
**Status:** ✅ Fixed

The loading dialog now properly displays the message and progress bar.

### Issue 5: GUI Doesn't Appear
**Possible causes:**
1. Tkinter not installed (it should come with Python)
2. Running in a headless environment

**Solution:**
Make sure you're running on a system with a display. Tkinter is included with standard Python installations on Windows.

## Verification Steps

### 1. Check Python Version
```bash
python --version
# Should be Python 3.7+
```

### 2. Check Dependencies
```bash
pip list | findstr "pdfplumber openpyxl pandas"
```

Should show:
- pdfplumber
- openpyxl
- pandas

### 3. Test Import
```bash
cd C:\Users\Omar\Desktop\magic
python -c "from src.main import main; print('Success')"
```

Should print: `Success`

### 4. Run Application
```bash
python run_app.py
```

The GUI should appear!

## File Structure Verification

Make sure your structure looks like this:

```
magic/
├── run_app.py          ← Run this file
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py     ← Important!
│   ├── main.py
│   ├── config/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   └── ui/
│       └── __init__.py
└── pdfs/
```

All `__init__.py` files must exist!

## Quick Fixes

### Reset to Clean State
If things aren't working:

1. Make sure you're in the right directory:
```bash
cd C:\Users\Omar\Desktop\magic
```

2. Check all __init__.py files exist:
```bash
find src -name "__init__.py"
```

Should show at least 7 `__init__.py` files.

3. Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

4. Run the app:
```bash
python run_app.py
```

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Check README.md for general usage
3. Verify all dependencies are installed
4. Ensure you're running from the project root

## Known Working Configuration

- **OS:** Windows 10/11
- **Python:** 3.7+
- **Run from:** `C:\Users\Omar\Desktop\magic\`
- **Command:** `python run_app.py`

## Success Indicators

When everything is working:

1. ✅ Command runs without errors
2. ✅ GUI window appears with title "Semi-Automated Balance Updater"
3. ✅ File selection buttons are visible
4. ✅ Type selection radio buttons (Stock/Free/Buy) are visible
5. ✅ All tabs are accessible
6. ✅ Loading dialog shows message and progress bar when extracting

---

**Last Updated:** After fixing import paths and loading dialog
