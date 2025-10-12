# How to Build a Standalone Windows Executable

## Option 1: Quick Build (Recommended)

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Run the Build Script
```bash
cd C:\Users\Omar\Desktop\magic
python build_executable.py
```

### Step 3: Find Your Executable
The executable will be created at:
```
C:\Users\Omar\Desktop\magic\dist\BalanceUpdater.exe
```

### Step 4: Distribute
Copy `BalanceUpdater.exe` to any Windows PC and run it! No Python installation needed!

---

## Option 2: Manual Build

### Build Single File Executable
```bash
cd C:\Users\Omar\Desktop\magic

pyinstaller --name=BalanceUpdater ^
            --onefile ^
            --windowed ^
            --add-data="src;src" ^
            --hidden-import=pdfplumber ^
            --hidden-import=pandas ^
            --hidden-import=openpyxl ^
            --hidden-import=tkinter ^
            run_app.py
```

### Build Directory (Faster startup)
```bash
pyinstaller --name=BalanceUpdater ^
            --windowed ^
            --add-data="src;src" ^
            --hidden-import=pdfplumber ^
            --hidden-import=pandas ^
            --hidden-import=openpyxl ^
            run_app.py
```

---

## Option 3: Create Installer (Professional)

### Using Inno Setup (Free)

1. **Download Inno Setup**: https://jrsoftware.org/isdl.php
2. **Install it**
3. **Create installer script** (see below)

### Inno Setup Script

Create `installer.iss`:

```iss
[Setup]
AppName=Balance Updater
AppVersion=2.0
DefaultDirName={pf}\BalanceUpdater
DefaultGroupName=Balance Updater
OutputDir=installer_output
OutputBaseFilename=BalanceUpdaterSetup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\BalanceUpdater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Balance Updater"; Filename: "{app}\BalanceUpdater.exe"
Name: "{commondesktop}\Balance Updater"; Filename: "{app}\BalanceUpdater.exe"

[Run]
Filename: "{app}\BalanceUpdater.exe"; Description: "Launch Balance Updater"; Flags: postinstall nowait skipifsilent
```

Then compile it with Inno Setup to create `BalanceUpdaterSetup.exe`

---

## Option 4: Using PyInstaller with Custom Icon

### Step 1: Get an Icon
- Create or download a `.ico` file
- Save as `icon.ico` in the project folder

### Step 2: Build with Icon
```bash
pyinstaller --name=BalanceUpdater ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="src;src" ^
            run_app.py
```

---

## Build Options Explained

### `--onefile`
- Creates a single `.exe` file
- Slower startup (extracts files to temp)
- Easier to distribute

### `--onedir` (default)
- Creates a folder with `.exe` and dependencies
- Faster startup
- Need to distribute whole folder

### `--windowed`
- No console window (GUI only)
- Use for final release

### `--console` (default)
- Shows console window
- Good for debugging

### `--add-data`
- Includes additional files/folders
- Format: `source;destination`

### `--hidden-import`
- Includes modules PyInstaller might miss
- Essential for tkinter, pandas, etc.

### `--icon`
- Sets the executable icon
- Use `.ico` format

---

## File Sizes

**Single File (--onefile):**
- Size: ~40-60 MB
- Includes Python + all libraries

**Directory (--onedir):**
- Size: ~50-70 MB (folder)
- Faster startup time

---

## Distribution Methods

### Method 1: Copy Executable
1. Build with `--onefile`
2. Copy `dist/BalanceUpdater.exe` to USB/network
3. Users double-click to run

### Method 2: ZIP File
1. Build with `--onedir`
2. ZIP the `dist/BalanceUpdater` folder
3. Users extract and run `BalanceUpdater.exe`

### Method 3: Installer
1. Create installer with Inno Setup
2. Users run `BalanceUpdaterSetup.exe`
3. Professional installation experience

### Method 4: Cloud Storage
1. Upload executable to Google Drive/OneDrive
2. Share download link
3. Users download and run

---

## Testing the Executable

### Test on Current PC
```bash
cd dist
BalanceUpdater.exe
```

### Test on Different PC (Important!)
1. Copy `.exe` to a PC **WITHOUT Python**
2. Double-click to run
3. Test all features

---

## Common Issues & Solutions

### Issue 1: "Failed to execute script"
**Solution:** Add missing imports
```bash
pyinstaller --hidden-import=missing_module run_app.py
```

### Issue 2: Slow Startup (--onefile)
**Solution:** Use `--onedir` instead
```bash
pyinstaller --onedir run_app.py
```

### Issue 3: Antivirus Blocks
**Solution:**
- Add exception in antivirus
- Or sign the executable (costs money)

### Issue 4: Large File Size
**Solution:** Normal! Python + libraries = big file
- Compress with UPX: `pyinstaller --upx-dir=PATH`
- Or accept the size

### Issue 5: Missing DLLs
**Solution:** Build on clean Windows with minimal software

---

## Advanced: Auto-Update System

### Using PyUpdater (Optional)

```bash
pip install pyupdater

pyupdater init
pyupdater build --app-version=2.0 run_app.py
pyupdater pkg --process
pyupdater upload --service s3
```

This creates an app that can auto-update itself!

---

## Quick Reference

### Minimal Build (Fast)
```bash
pyinstaller --onefile --windowed run_app.py
```

### Full Build (Recommended)
```bash
python build_executable.py
```

### Professional Build
```bash
pyinstaller --name=BalanceUpdater ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="src;src" ^
            --version-file=version.txt ^
            run_app.py
```

---

## What Gets Included

The executable includes:
- ✅ Python interpreter
- ✅ All your code (`src/` folder)
- ✅ All dependencies (pdfplumber, pandas, openpyxl)
- ✅ tkinter (GUI framework)

Users need:
- ❌ Nothing! Just Windows

---

## Size Optimization Tips

1. **Use virtual environment** (only needed packages)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller ...
```

2. **Exclude unused modules**
```bash
pyinstaller --exclude-module=matplotlib run_app.py
```

3. **Use UPX compression**
- Download UPX: https://upx.github.io/
- Extract to folder
- Use: `pyinstaller --upx-dir=C:\upx run_app.py`

---

## Creating a Version File

### version.txt
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'Balance Updater Application'),
        StringStruct(u'FileVersion', u'2.0.0.0'),
        StringStruct(u'InternalName', u'BalanceUpdater'),
        StringStruct(u'ProductName', u'Balance Updater'),
        StringStruct(u'ProductVersion', u'2.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Then build with:
```bash
pyinstaller --version-file=version.txt run_app.py
```

---

## Summary

**Easiest Way:**
```bash
pip install pyinstaller
python build_executable.py
```

**Result:**
→ `dist/BalanceUpdater.exe` (40-60 MB)
→ Works on any Windows PC
→ No Python required
→ Double-click to run!

**Share it:**
→ Copy to USB drive
→ Upload to cloud
→ Email to colleagues
→ Create installer

Done! 🎉
