"""Text cleaning and normalization utilities."""

import re
from typing import Optional


def fix_doubled_chars(text: Optional[str]) -> Optional[str]:
    """
    Fix text with doubled characters (common PDF extraction issue).

    Takes every other character to fix duplication artifacts from PDF parsing.
    Example: "HHeelllloo" -> "Hello"

    Args:
        text: Input text that may contain doubled characters

    Returns:
        Text with doubled characters removed, or None if input is None
    """
    if not text:
        return text
    return ''.join([text[i] for i in range(0, len(text), 2)])


def clean_text(text: str) -> str:
    """
    Clean and normalize text for pattern matching.

    Removes whitespace, standardizes dashes, and applies doubled char fix.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned and normalized text
    """
    if not text:
        return ""

    # Remove all whitespace
    text_no_spaces = re.sub(r'\s+', '', text)

    # Standardize different dash types to regular dash
    text_std_dashes = text_no_spaces.replace('–', '-').replace('—', '-')

    # Fix doubled characters
    cleaned = fix_doubled_chars(text_std_dashes)

    return cleaned if cleaned else ""
