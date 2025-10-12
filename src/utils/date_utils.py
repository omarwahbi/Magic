"""Date parsing and validation utilities."""

from datetime import datetime
from typing import Optional, Tuple
import re
from src.utils.regex_patterns import DATE_PATTERN


def parse_expiry_date(text: str) -> Optional[Tuple[int, int, int]]:
    """
    Extract and parse expiry date from text.

    Args:
        text: Text that may contain a date in DD/MM/YYYY format

    Returns:
        Tuple of (day, month, year) if date found and valid, None otherwise
    """
    match = DATE_PATTERN.search(text)
    if not match:
        return None

    try:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))

        # Basic validation
        if not (1 <= day <= 31 and 1 <= month <= 12 and year >= 1900):
            return None

        return (day, month, year)
    except (ValueError, IndexError):
        return None


def is_expired(day: int, month: int, year: int) -> bool:
    """
    Check if a date is expired (before current month).

    Args:
        day: Day of the month
        month: Month (1-12)
        year: Year (4 digits)

    Returns:
        True if the date is expired, False otherwise
    """
    now = datetime.now()
    return year < now.year or (year == now.year and month < now.month)


def format_date(day: int, month: int, year: int) -> str:
    """
    Format date components as DD/MM/YYYY string.

    Args:
        day: Day of the month
        month: Month (1-12)
        year: Year (4 digits)

    Returns:
        Formatted date string
    """
    return f"{day}/{month}/{year}"
