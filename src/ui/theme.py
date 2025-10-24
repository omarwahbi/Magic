"""
Modern theme system for Magic app.

Provides colors, typography, spacing, and component styles for consistent UI.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class Colors:
    """Color palette for the application."""

    # Primary colors
    primary: str = "#6366F1"  # Indigo - Magic, trust, professionalism
    primary_dark: str = "#4F46E5"
    primary_light: str = "#818CF8"

    # Semantic colors
    success: str = "#10B981"  # Emerald - Matched items, success
    success_dark: str = "#059669"
    success_light: str = "#34D399"

    warning: str = "#F59E0B"  # Amber - Warnings, cross-page issues
    warning_dark: str = "#D97706"
    warning_light: str = "#FBBF24"

    error: str = "#EF4444"  # Red - Errors, missing items
    error_dark: str = "#DC2626"
    error_light: str = "#F87171"

    info: str = "#3B82F6"  # Blue - Information, guidance
    info_dark: str = "#2563EB"
    info_light: str = "#60A5FA"

    # Neutral colors
    background: str = "#F9FAFB"  # Light gray background
    surface: str = "#FFFFFF"  # White cards/surfaces
    border: str = "#E5E7EB"  # Light gray borders

    text: str = "#111827"  # Dark gray - primary text
    text_secondary: str = "#6B7280"  # Medium gray - secondary text
    text_disabled: str = "#9CA3AF"  # Light gray - disabled text

    # Hover states
    hover_bg: str = "#F3F4F6"
    hover_border: str = "#D1D5DB"


@dataclass
class Typography:
    """Typography system for the application."""

    # Font families
    font_family: str = "Segoe UI"
    font_family_mono: str = "Consolas"

    # Font sizes
    heading_1: int = 24
    heading_2: int = 20
    heading_3: int = 16
    body: int = 14
    caption: int = 12
    small: int = 11

    # Font weights
    weight_normal: str = "normal"
    weight_semibold: str = "bold"  # ttk doesn't support actual semibold
    weight_bold: str = "bold"


@dataclass
class Spacing:
    """Spacing system based on 8px grid."""

    xs: int = 4   # Tight spacing
    sm: int = 8   # Default spacing
    md: int = 16  # Section spacing
    lg: int = 24  # Component spacing
    xl: int = 32  # Major section spacing
    xxl: int = 48 # Page spacing


@dataclass
class BorderRadius:
    """Border radius values for rounded corners."""

    sm: int = 4   # Small radius (buttons, inputs)
    md: int = 8   # Medium radius (cards)
    lg: int = 12  # Large radius (modals)
    full: int = 999  # Fully rounded (pills, badges)


class Theme:
    """Main theme class providing all styling constants."""

    def __init__(self):
        self.colors = Colors()
        self.typography = Typography()
        self.spacing = Spacing()
        self.radius = BorderRadius()

    # Component-specific styles
    @property
    def button_primary(self) -> Dict[str, str]:
        """Primary button style."""
        return {
            "background": self.colors.primary,
            "foreground": "#FFFFFF",
            "borderwidth": 0,
            "relief": "flat",
            "padding": (self.spacing.md, self.spacing.sm),
        }

    @property
    def button_secondary(self) -> Dict[str, str]:
        """Secondary button style."""
        return {
            "background": self.colors.surface,
            "foreground": self.colors.text,
            "borderwidth": 1,
            "relief": "solid",
            "padding": (self.spacing.md, self.spacing.sm),
        }

    @property
    def card(self) -> Dict[str, str]:
        """Card container style."""
        return {
            "background": self.colors.surface,
            "borderwidth": 1,
            "relief": "solid",
            "padding": self.spacing.md,
        }

    @property
    def status_success(self) -> Dict[str, str]:
        """Success status badge style."""
        return {
            "background": self.colors.success_light,
            "foreground": self.colors.success_dark,
        }

    @property
    def status_warning(self) -> Dict[str, str]:
        """Warning status badge style."""
        return {
            "background": self.colors.warning_light,
            "foreground": self.colors.warning_dark,
        }

    @property
    def status_error(self) -> Dict[str, str]:
        """Error status badge style."""
        return {
            "background": self.colors.error_light,
            "foreground": self.colors.error_dark,
        }


# Global theme instance
theme = Theme()


# Icon/emoji mappings for consistent use
class Icons:
    """Unicode emoji icons for the application."""

    # General
    MAGIC = "✨"
    APP_ICON = "📊"

    # File operations
    FOLDER = "📁"
    FILE = "📄"
    PDF = "📕"
    EXCEL = "📗"

    # Actions
    SEARCH = "🔍"
    SETTINGS = "⚙️"
    HELP = "ℹ️"
    REFRESH = "↻"
    DOWNLOAD = "⬇️"
    UPLOAD = "⬆️"

    # Status
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠️"
    INFO = "ℹ️"

    # Data
    CHART = "📊"
    TABLE = "📋"
    LIST = "📝"

    # UI elements
    CLOSE = "×"
    MENU = "☰"
    ARROW_RIGHT = "→"
    ARROW_DOWN = "↓"

    # Extraction types
    STOCK = "📦"
    FREE = "🎁"
    BUY = "🛒"


icons = Icons()
