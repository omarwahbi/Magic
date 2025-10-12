"""Application-wide settings and configuration."""

import logging
from dataclasses import dataclass
from typing import Tuple


@dataclass
class LoggingConfig:
    """Logging configuration."""
    filename: str = 'extraction_log.txt'
    level: int = logging.WARNING
    filemode: str = 'w'  # Overwrite log file each time
    format: str = '%(asctime)s - %(levelname)s - %(message)s'

    def configure(self) -> None:
        """Apply logging configuration."""
        logging.basicConfig(
            filename=self.filename,
            level=self.level,
            filemode=self.filemode,
            format=self.format
        )


@dataclass
class AppSettings:
    """Application settings."""

    # UI Settings
    WINDOW_TITLE: str = "Semi-Automated Balance Updater"
    WINDOW_SIZE: Tuple[int, int] = (900, 700)

    # Excel Settings
    EXCEL_START_ROW: int = 2  # Data starts at row 2 (skip header)
    CODE_COLUMN: int = 0  # National code is in first column (0-based)

    # File Patterns
    PDF_PATTERN: str = "*.pdf"
    EXCEL_PATTERN: str = "*.xlsx *.xls"

    # Output Settings
    OUTPUT_FILE_PREFIX: str = "updated_medicines"
    OUTPUT_DATE_FORMAT: str = "%Y%m%d_%H%M%S"

    # Tree View Settings
    TREE_HEIGHT: int = 15

    # Colors
    COLOR_SUCCESS: str = "#d4edda"
    COLOR_MISSING: str = "#f8d7da"
    COLOR_PRIMARY: str = "#2196F3"
    COLOR_SUCCESS_BTN: str = "#4CAF50"
    COLOR_WARNING: str = "#FF9800"
