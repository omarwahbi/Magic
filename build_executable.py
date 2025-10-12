"""
Script to build standalone Windows executable using PyInstaller.

This creates a single executable file that includes Python and all dependencies.
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller installed\n")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=BalanceUpdater",              # Name of the executable
        "--onefile",                           # Single file
        "--windowed",                          # No console window
        "--icon=NONE",                         # You can add an icon later
        "--add-data=src;src",                  # Include src directory
        "--hidden-import=pdfplumber",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "run_app.py"                           # Main script
    ]

    subprocess.check_call(cmd)
    print("\n✓ Build complete!")
    print("\nExecutable location: dist/BalanceUpdater.exe")

def main():
    print("=" * 60)
    print("Balance Updater - Executable Builder")
    print("=" * 60)
    print()

    try:
        # Check if PyInstaller is installed
        try:
            import PyInstaller
            print("✓ PyInstaller already installed\n")
        except ImportError:
            install_pyinstaller()

        # Build the executable
        build_executable()

        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("\nYour executable is ready at: dist/BalanceUpdater.exe")
        print("\nYou can:")
        print("1. Copy BalanceUpdater.exe to any Windows PC")
        print("2. Double-click to run (no Python needed!)")
        print("3. Share with others")
        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease make sure you have all dependencies installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
