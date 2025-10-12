@echo off
echo ============================================
echo Balance Updater - Build Executable
echo ============================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

echo Building executable...
echo.

REM Build the executable
pyinstaller --name=BalanceUpdater --onefile --windowed --add-data="src;src" --hidden-import=pdfplumber --hidden-import=pandas --hidden-import=openpyxl --hidden-import=tkinter run_app.py

echo.
echo ============================================
echo BUILD COMPLETE!
echo ============================================
echo.
echo Your executable is ready at:
echo dist\BalanceUpdater.exe
echo.
echo File size: ~40-60 MB
echo.
echo You can now:
echo - Copy BalanceUpdater.exe to any Windows PC
echo - Double-click to run (no Python needed!)
echo - Share with others
echo.
echo ============================================
pause
