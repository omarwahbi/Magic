"""Settings dialog for configuring Excel column mappings."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Callable, Optional

from src.ui.theme import theme, icons
from src.services.settings_manager import SettingsManager


class SettingsDialog:
    """Modal dialog for application settings."""

    # Available columns A-Z
    COLUMNS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    def __init__(self, parent: tk.Widget, on_save: Optional[Callable] = None):
        """
        Initialize the settings dialog.

        Args:
            parent: Parent widget
            on_save: Optional callback when settings are saved
        """
        self.parent = parent
        self.on_save = on_save
        self.result = False
        
        # Create modal dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{icons.SETTINGS} Settings")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Set size and center
        dialog_width = 400
        dialog_height = 500
        x = parent.winfo_rootx() + (parent.winfo_width() - dialog_width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - dialog_height) // 2
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.dialog.resizable(True, True)
        
        # Style
        self.dialog.configure(bg=theme.colors.background)
        
        # Build UI
        self._create_widgets()
        self._load_current_settings()
        
        # Handle close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _create_widgets(self):
        """Create all dialog widgets."""
        # Main container with padding
        main_frame = tk.Frame(
            self.dialog,
            bg=theme.colors.background,
            padx=theme.spacing.lg,
            pady=theme.spacing.lg
        )
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Create buttons frame first and pack at BOTTOM
        # This ensures they are always allocated space first
        buttons_frame = tk.Frame(main_frame, bg=theme.colors.background)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(theme.spacing.md, 0))

        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            command=self._on_cancel,
            font=(theme.typography.font_family, theme.typography.body),
            bg=theme.colors.surface,
            fg=theme.colors.text,
            relief=tk.FLAT,
            borderwidth=1,
            padx=theme.spacing.md,
            pady=theme.spacing.xs,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(theme.spacing.sm, 0))

        # Save button
        save_btn = tk.Button(
            buttons_frame,
            text=f"{icons.SUCCESS} Save",
            command=self._on_save,
            font=(theme.typography.font_family, theme.typography.body, "bold"),
            bg=theme.colors.primary,
            fg="white",
            relief=tk.FLAT,
            padx=theme.spacing.md,
            pady=theme.spacing.xs,
            cursor="hand2"
        )
        save_btn.pack(side=tk.RIGHT)

        # 2. Create content frame for the rest
        content_frame = tk.Frame(main_frame, bg=theme.colors.background)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            content_frame,
            text=f"{icons.EXCEL} Excel Column Mappings",
            font=(theme.typography.font_family, theme.typography.heading_3, "bold"),
            bg=theme.colors.background,
            fg=theme.colors.text
        )
        title_label.pack(anchor=tk.W, pady=(0, theme.spacing.sm))

        # Description
        desc_label = tk.Label(
            content_frame,
            text="Configure which Excel columns receive extracted data:",
            font=(theme.typography.font_family, theme.typography.caption),
            bg=theme.colors.background,
            fg=theme.colors.text_secondary,
            wraplength=300,
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, pady=(0, theme.spacing.md))

        # Column mappings frame
        mappings_frame = tk.Frame(content_frame, bg=theme.colors.surface,
                                  highlightbackground=theme.colors.border,
                                  highlightthickness=1,
                                  padx=theme.spacing.sm,
                                  pady=theme.spacing.sm)
        mappings_frame.pack(fill=tk.X, pady=(0, theme.spacing.lg))

        # Dropdown variables
        self.free_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.buy_var = tk.StringVar()

        # Create dropdowns for each type
        self._create_mapping_row(mappings_frame, f"{icons.FREE} Free", self.free_var, 0)
        self._create_mapping_row(mappings_frame, f"{icons.STOCK} Stock", self.stock_var, 1)
        self._create_mapping_row(mappings_frame, f"{icons.BUY} Buy", self.buy_var, 2)

    def _create_mapping_row(self, parent: tk.Frame, label_text: str, 
                           variable: tk.StringVar, row: int):
        """Create a single mapping row with label and dropdown."""
        row_frame = tk.Frame(parent, bg=theme.colors.surface)
        row_frame.pack(fill=tk.X, padx=theme.spacing.md, pady=theme.spacing.md)

        # Label
        label = tk.Label(
            row_frame,
            text=label_text,
            font=(theme.typography.font_family, theme.typography.body),
            bg=theme.colors.surface,
            fg=theme.colors.text,
            width=12,
            anchor=tk.W
        )
        label.pack(side=tk.LEFT)

        # Arrow
        arrow = tk.Label(
            row_frame,
            text=icons.ARROW_RIGHT,
            font=(theme.typography.font_family, theme.typography.body),
            bg=theme.colors.surface,
            fg=theme.colors.text_secondary
        )
        arrow.pack(side=tk.LEFT, padx=theme.spacing.sm)

        # Column label
        col_label = tk.Label(
            row_frame,
            text="Column:",
            font=(theme.typography.font_family, theme.typography.body),
            bg=theme.colors.surface,
            fg=theme.colors.text
        )
        col_label.pack(side=tk.LEFT, padx=(0, theme.spacing.sm))

        # Dropdown using OptionMenu for better visibility
        dropdown = tk.OptionMenu(
            row_frame,
            variable,
            *self.COLUMNS
        )
        dropdown.config(
            font=(theme.typography.font_family, theme.typography.body),
            bg=theme.colors.surface,
            fg=theme.colors.text,
            activebackground=theme.colors.primary,
            activeforeground="white",
            highlightthickness=1,
            highlightbackground=theme.colors.border,
            width=3
        )
        dropdown.pack(side=tk.LEFT)

    def _load_current_settings(self):
        """Load current column mappings into dropdowns."""
        mappings = SettingsManager.get_column_mappings()
        self.free_var.set(mappings.get("Free", "G"))
        self.stock_var.set(mappings.get("Stock", "H"))
        self.buy_var.set(mappings.get("Buy", "I"))

    def _get_current_mappings(self) -> Dict[str, str]:
        """Get current dropdown values as mappings dict."""
        return {
            "Free": self.free_var.get(),
            "Stock": self.stock_var.get(),
            "Buy": self.buy_var.get()
        }

    def _on_save(self):
        """Handle save button click."""
        mappings = self._get_current_mappings()
        
        # Validate
        is_valid, error = SettingsManager.validate_column_mappings(mappings)
        if not is_valid:
            messagebox.showerror("Validation Error", error, parent=self.dialog)
            return
        
        # Save
        SettingsManager.save_column_mappings(mappings)
        self.result = True
        
        # Callback
        if self.on_save:
            self.on_save()
        
        self.dialog.destroy()

    def _on_cancel(self):
        """Handle cancel/close."""
        self.dialog.destroy()

    def show(self) -> bool:
        """
        Show the dialog and wait for it to close.
        
        Returns:
            True if settings were saved, False if cancelled
        """
        self.dialog.wait_window()
        return self.result
