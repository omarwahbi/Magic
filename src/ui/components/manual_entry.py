"""Manual entry widget for correcting balances."""

import tkinter as tk
from typing import Callable, Optional


class ManualEntryWidget:
    """Widget for manual balance entry and correction."""

    def __init__(
        self,
        parent: tk.Widget,
        on_update: Callable[[float], None],
        button_color: str = "#4CAF50"
    ):
        """
        Initialize manual entry widget.

        Args:
            parent: Parent widget
            on_update: Callback when update button is clicked (receives balance value)
            button_color: Update button color
        """
        self.on_update = on_update
        self.frame = tk.Frame(parent, padx=10, pady=10)

        # Label
        tk.Label(self.frame, text="Manual correction:").pack(side="left", padx=5)

        # Balance label
        tk.Label(self.frame, text="Balance:").pack(side="left")

        # Entry field
        self.entry = tk.Entry(self.frame, width=15)
        self.entry.pack(side="left", padx=5)

        # Update button
        self.button = tk.Button(
            self.frame,
            text="Update Selected",
            command=self._on_update_clicked,
            bg=button_color,
            fg="white"
        )
        self.button.pack(side="left", padx=5)

    def pack(self, **kwargs) -> None:
        """Pack the widget frame."""
        self.frame.pack(**kwargs)

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
