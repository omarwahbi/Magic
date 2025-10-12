"""Manual entry widget for correcting balances."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class ManualEntryWidget(ttk.Frame):
    """Widget for manual balance entry and correction."""

    def __init__(
        self,
        parent: tk.Widget,
        on_update: Callable[[float], None],
        **kwargs
    ):
        """
        Initialize manual entry widget.

        Args:
            parent: Parent widget
            on_update: Callback when update button is clicked (receives balance value)
        """
        super().__init__(parent, padding=(10, 5), **kwargs)
        self.on_update = on_update

        # Label
        ttk.Label(self, text="Manual correction:").pack(side="left", padx=5)

        # Balance label
        ttk.Label(self, text="Balance:").pack(side="left")

        # Entry field
        self.entry = ttk.Entry(self, width=15)
        self.entry.pack(side="left", padx=5)

        # Update button
        self.button = ttk.Button(
            self,
            text="Update Selected",
            command=self._on_update_clicked,
            style="Accent.TButton"
        )
        self.button.pack(side="left", padx=5)



    def get_value(self) -> Optional[float]:
        """
        Get the entered value as float.

        Returns:
            Float value or None if invalid/empty
        """
        value = self.entry.get().strip()
        if not value:
            return None

        try:
            return float(value)
        except ValueError:
            return None

    def clear(self) -> None:
        """Clear the entry field."""
        self.entry.delete(0, tk.END)

    def _on_update_clicked(self) -> None:
        """Handle update button click."""
        value = self.get_value()
        if value is not None:
            self.on_update(value)
            self.clear()
