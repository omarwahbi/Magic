"""Type selector component for extraction type (Stock/Free/Buy)."""

import tkinter as tk
from typing import Callable, Optional

from src.config.extraction_config import ExtractionType


import tkinter as tk
from typing import Callable, Optional

from src.config.extraction_config import ExtractionType


class TypeSelector(tk.Frame):
    """Widget for selecting extraction type."""

    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        default_value: str = "Stock",
        on_change: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize type selector.

        Args:
            parent: Parent widget
            label_text: Text for the main label.
            default_value: Default extraction type
            on_change: Callback when selection changes
        """
        super().__init__(parent, **kwargs)
        self.on_change = on_change
        self.value = tk.StringVar(value=default_value)

        # Label
        tk.Label(self, text=label_text).pack(side="left")

        # Radio buttons
        for extraction_type in ExtractionType:
            tk.Radiobutton(
                self,
                text=extraction_type.value,
                variable=self.value,
                value=extraction_type.value,
                command=self._on_select
            ).pack(side="left", padx=5)


    def get_value(self) -> str:
        """Get selected extraction type value."""
        return self.value.get()

    def get_extraction_type(self) -> ExtractionType:
        """Get selected extraction type as enum."""
        from src.config.extraction_config import ExtractionConfig
        return ExtractionConfig.from_string(self.value.get())

    def _on_select(self) -> None:
        """Handle radio button selection."""
        if self.on_change:
            self.on_change(self.value.get())
