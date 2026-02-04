"""
Manages loading and saving of application settings to a JSON file.
"""

import json
import os
import logging
from typing import Dict, Any

SETTINGS_FILE = "settings.json"

# Default column mappings (letter format)
DEFAULT_COLUMN_MAPPINGS = {
    "Free": "G",
    "Stock": "H",
    "Buy": "I"
}


class SettingsManager:
    """Handles reading from and writing to the settings.json file."""

    @staticmethod
    def column_letter_to_index(letter: str) -> int:
        """
        Convert Excel column letter to 0-based index.
        
        Args:
            letter: Column letter (A-Z)
            
        Returns:
            0-based column index (A=0, B=1, ..., Z=25)
        """
        return ord(letter.upper()) - ord('A')

    @staticmethod
    def get_column_mappings() -> Dict[str, str]:
        """
        Get column mappings from settings.
        
        Returns:
            Dictionary mapping extraction type to column letter.
        """
        settings = SettingsManager.load_settings()
        mappings = settings.get("column_mappings", {})
        
        # Merge with defaults for any missing keys
        result = DEFAULT_COLUMN_MAPPINGS.copy()
        for key in DEFAULT_COLUMN_MAPPINGS:
            if key in mappings and mappings[key]:
                result[key] = mappings[key].upper()
        
        return result

    @staticmethod
    def save_column_mappings(mappings: Dict[str, str]) -> None:
        """
        Save column mappings to settings.
        
        Args:
            mappings: Dictionary mapping extraction type to column letter.
        """
        settings = SettingsManager.load_settings()
        settings["column_mappings"] = {k: v.upper() for k, v in mappings.items()}
        SettingsManager.save_settings(settings)

    @staticmethod
    def validate_column_mappings(mappings: Dict[str, str]) -> tuple[bool, str]:
        """
        Validate that column mappings are valid and not duplicated.
        
        Args:
            mappings: Dictionary mapping extraction type to column letter.
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        columns_used = []
        for type_name, column in mappings.items():
            # Check if column is valid (A-Z)
            if not column or len(column) != 1 or not column.upper().isalpha():
                return False, f"Invalid column '{column}' for {type_name}. Use A-Z."
            
            col_upper = column.upper()
            if col_upper in columns_used:
                return False, f"Column {col_upper} is assigned to multiple types."
            columns_used.append(col_upper)
        
        return True, ""

    @staticmethod
    def load_settings() -> Dict[str, Any]:
        """
        Load settings from settings.json.

        Returns:
            A dictionary with the settings, or an empty dict if file not found.
        """
        if not os.path.exists(SETTINGS_FILE):
            logging.warning(f"Settings file not found at: {SETTINGS_FILE}")
            return {}
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Failed to load settings from {SETTINGS_FILE}: {e}")
            return {}

    @staticmethod
    def save_settings(settings: Dict[str, Any]) -> None:
        """
        Save the provided dictionary to settings.json.

        Args:
            settings: The dictionary of settings to save.
        """
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
            logging.info(f"Settings saved successfully to {SETTINGS_FILE}")
        except IOError as e:
            logging.error(f"Failed to save settings to {SETTINGS_FILE}: {e}")
