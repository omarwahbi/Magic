"""
Semi-Automated Balance Updater

Main entry point for the refactored modular application.

This application extracts pharmaceutical balance data from PDF files
and updates Excel spreadsheets with the extracted information.

Usage:
    From project root: python run_app.py
    Or: python -m src.main
"""

import sys
import os
from pathlib import Path

# Ensure src directory is in the path
src_dir = Path(__file__).parent
if str(src_dir.parent) not in sys.path:
    sys.path.insert(0, str(src_dir.parent))

import tkinter as tk
from src.ui.main_window import BalanceUpdaterApp
import sv_ttk


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    sv_ttk.set_theme("light")
    app = BalanceUpdaterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
