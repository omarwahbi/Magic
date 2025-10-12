"""
Convenience script to run the application from the project root.

Usage:
    python run_app.py
"""

import sys
import os
from pathlib import Path

# Add project root to path so 'src' can be imported as a package
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run
from src.main import main

if __name__ == "__main__":
    main()
