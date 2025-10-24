# Magic - Build Guide

## Table of Contents
1. [Quick Build](#quick-build)
2. [Prerequisites](#prerequisites)
3. [Detailed Build Instructions](#detailed-build-instructions)
4. [Build Options](#build-options)
5. [Distribution](#distribution)
6. [Troubleshooting Build Issues](#troubleshooting-build-issues)

---

## Quick Build

### Fastest Method (Windows)
```bash
# Double-click this file:
build.bat
```

**Output:** `dist/Magic.exe`

---

## Prerequisites

### Required Software
1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Dependencies**
   - Install from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **PyInstaller**
   - Included in `requirements.txt`
   - Or install separately:
   ```bash
   pip install pyinstaller
   ```

### Verify Installation
```bash
python --version       # Should show Python 3.8+
pip --version          # Should show pip version
pyinstaller --version  # Should show PyInstaller version
```

---

## Detailed Build Instructions

### Method 1: Using build.bat (Windows - Recommended)

1. **Navigate to project root:**
   ```bash
   cd "C:\Users\Omar\Desktop\magic - refractored"
   ```

2. **Run build script:**
   ```bash
   build.bat
   ```

3. **Find executable:**
   ```
   dist/Magic.exe
   ```

**What build.bat does:**
- Installs/updates PyInstaller
- Runs PyInstaller with correct settings
- Creates standalone executable in `dist/` folder
- Includes all dependencies

---

### Method 2: Using build_executable.py

1. **Navigate to project root:**
   ```bash
   cd "C:\Users\Omar\Desktop\magic - refractored"
   ```

2. **Run build script:**
   ```bash
   python build_executable.py
   ```

3. **Find executable:**
   ```
   dist/Magic.exe
   ```

**What build_executable.py does:**
- Python script for cross-platform builds
- Same functionality as build.bat
- Works on Windows, macOS, Linux

---

### Method 3: Manual PyInstaller Command

For advanced users who want full control:

```bash
pyinstaller --clean --onefile --windowed --name=Magic ^
  --add-data="src;src" ^
  --hidden-import=pdfplumber ^
  --hidden-import=pandas ^
  --hidden-import=openpyxl ^
  run_app.py
```

**Explanation of flags:**
- `--clean`: Remove temporary files before building
- `--onefile`: Create a single executable file
- `--windowed`: No console window (GUI only)
- `--name=Magic`: Name the executable "Magic.exe"
- `--add-data="src;src"`: Include src directory
- `--hidden-import`: Ensure specific modules are included

---

## Build Options

### Creating Console Build (For Debugging)
```bash
pyinstaller --clean --onefile --name=Magic ^
  --add-data="src;src" ^
  run_app.py
```

**Note:** Remove `--windowed` to see console output and error messages.

### Creating Folder Distribution (Faster Startup)
```bash
pyinstaller --clean --windowed --name=Magic ^
  --add-data="src;src" ^
  run_app.py
```

**Note:** Remove `--onefile` to create a folder with executable + dependencies.
- **Pros:** Faster startup time
- **Cons:** Multiple files to distribute

### Custom Icon (Optional)
```bash
pyinstaller --clean --onefile --windowed --name=Magic ^
  --icon=icon.ico ^
  --add-data="src;src" ^
  run_app.py
```

**Note:** Add your own `icon.ico` file to customize the executable icon.

---

## Distribution

### Single Executable Distribution (Current Setup)

**What to distribute:**
```
dist/
└── Magic.exe    # Single file - ready to use!
```

**Advantages:**
- Single file - easy to share
- No installation required
- Works on any Windows PC (no Python needed)

**How to distribute:**
1. Locate `dist/Magic.exe`
2. Copy to USB drive, network share, or compress to ZIP
3. Users can run directly - no setup required

---

### Folder Distribution (Alternative)

If using folder build (without `--onefile`):

**What to distribute:**
```
dist/Magic/
├── Magic.exe           # Main executable
├── _internal/          # Dependencies folder
│   ├── python3.dll
│   ├── library.zip
│   └── ... (other files)
└── (other support files)
```

**Advantages:**
- Faster startup (no unpacking)
- Easier to debug

**How to distribute:**
1. Compress entire `dist/Magic/` folder to ZIP
2. Users extract and run `Magic.exe`

---

### Installer Creation (Advanced)

For professional distribution, create an installer using:

**Option 1: Inno Setup (Windows)**
- Download: https://jrsoftware.org/isinfo.php
- Free and easy to use
- Creates professional Windows installer

**Option 2: NSIS**
- Download: https://nsis.sourceforge.io/
- More complex but powerful

**Option 3: WiX Toolset**
- Download: https://wixtoolset.org/
- Most professional, steepest learning curve

---

## Troubleshooting Build Issues

### Issue: "pyinstaller: command not found"
**Solution:**
```bash
pip install pyinstaller
```

### Issue: "Module not found" during build
**Solution:** Add hidden import:
```bash
pyinstaller ... --hidden-import=module_name ...
```

### Issue: Build succeeds but executable crashes
**Solutions:**
1. **Run console build to see errors:**
   ```bash
   pyinstaller --clean --onefile run_app.py
   ```
   Then run `dist/run_app.exe` from command line to see error messages.

2. **Check for missing data files:**
   - Ensure `--add-data="src;src"` is included
   - Add other data files if needed

3. **Check for missing dependencies:**
   - Verify all imports are in `requirements.txt`
   - Add `--hidden-import` for problematic modules

### Issue: Executable is too large
**Solutions:**
1. **Use folder distribution instead of --onefile**
2. **Exclude unnecessary modules:**
   ```bash
   pyinstaller ... --exclude-module=tkinter.test ...
   ```
3. **Use UPX compression:**
   - Download UPX: https://upx.github.io/
   - Place in PATH
   - PyInstaller will automatically compress

### Issue: Antivirus flags the executable
**Explanation:** Common with PyInstaller executables (false positive).

**Solutions:**
1. **Add exception in antivirus software**
2. **Code sign the executable** (requires certificate)
3. **Build with different Python version**
4. **Use folder distribution instead of --onefile**

### Issue: "Failed to execute script" error
**Solution:** Run from command line to see full error:
```bash
cd dist
Magic.exe
```

Then fix the reported error (usually missing module or data file).

### Issue: Build very slow
**Solutions:**
1. **Clean old builds:**
   ```bash
   rmdir /s /q build dist
   del *.spec
   ```
2. **Disable antivirus temporarily** (scans slow down build)
3. **Use SSD instead of HDD** if possible

---

## Build Files Explained

### BalanceUpdater.spec
- PyInstaller specification file
- Auto-generated on first build
- Can be edited for custom build configurations
- Rerun with: `pyinstaller BalanceUpdater.spec`

### build/ folder
- Temporary build files
- Can be safely deleted
- Auto-recreated on next build

### dist/ folder
- Final executable location
- **Magic.exe** is here
- This is what you distribute

---

## Advanced Build Configuration

### Editing .spec File

For repeated builds with custom options:

1. **Generate .spec file:**
   ```bash
   pyi-makespec --onefile --windowed --name=Magic run_app.py
   ```

2. **Edit Magic.spec** to customize build

3. **Build from .spec:**
   ```bash
   pyinstaller Magic.spec
   ```

### Multi-Platform Builds

**Windows:**
- Build on Windows → Creates `.exe`

**macOS:**
- Build on macOS → Creates `.app` bundle
- Same commands, different output

**Linux:**
- Build on Linux → Creates executable binary
- Same commands, different output

**Note:** PyInstaller executables are NOT cross-platform. Build on each target OS.

---

## Continuous Integration (CI)

### GitHub Actions Example

Create `.github/workflows/build.yml`:

```yaml
name: Build

on: [push]

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - run: pip install -r requirements.txt
    - run: python build_executable.py
    - uses: actions/upload-artifact@v2
      with:
        name: Magic-Windows
        path: dist/Magic.exe
```

---

## Build Checklist

Before distributing the executable:

- [ ] Test extraction with Stock type
- [ ] Test extraction with Free type
- [ ] Test extraction with Buy type
- [ ] Test file selection (PDF + Excel)
- [ ] Test manual entry
- [ ] Test all export options
- [ ] Test save functionality
- [ ] Test view log button
- [ ] Test on clean Windows PC (no Python installed)
- [ ] Check executable size (reasonable?)
- [ ] Scan with antivirus (verify no false positives)

---

## Need Help?

If build fails:
1. Check error message carefully
2. Review this guide's troubleshooting section
3. Try console build to see full errors
4. Verify all dependencies are installed
5. Check `TROUBLESHOOTING.md` for common issues
