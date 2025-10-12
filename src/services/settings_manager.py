"""
Manages loading and saving of application settings to a JSON file.
"""

import json
import os
import logging
from typing import Dict, Any

SETTINGS_FILE = "settings.json"

class SettingsManager:
    """Handles reading from and writing to the settings.json file."""

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
