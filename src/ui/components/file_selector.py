import tkinter as tk
from tkinter import ttk, filedialog
from typing import List, Optional, Callable
import os


class FileSelector(ttk.Frame):
    """Widget for selecting PDF or Excel files."""

    def __init__(
        self,
        parent: tk.Widget,
        label_text: str,
        button_text: str,
        file_types: List[tuple],
        multiple: bool = False,
        on_select: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize file selector.

        Args:
            parent: Parent widget
            label_text: Label text (e.g., "PDFs:")
            button_text: Button text (e.g., "Browse")
            file_types: File type filters for dialog
            multiple: Whether to allow multiple file selection
            on_select: Callback when files are selected
        """
        super().__init__(parent, **kwargs)
        self.multiple = multiple
        self.file_types = file_types
        self.on_select = on_select
        self.selected_files: List[str] = [] if multiple else []
        self.selected_file: Optional[str] = None

        self.columnconfigure(1, weight=1)

        # Create label
        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, sticky="w")

        # Create status label
        self.status_label = ttk.Label(
            self,
            text="No files selected" if multiple else "No file selected",
            anchor="w"
        )
        self.status_label.grid(row=0, column=1, sticky="ew", padx=5)

        # Create browse button
        self.button = ttk.Button(
            self,
            text=button_text,
            command=self._browse,
        )
        self.button.grid(row=0, column=2, padx=5)


    def _browse(self) -> None:
        """Open file dialog and handle selection."""
        if self.multiple:
            files = filedialog.askopenfilenames(filetypes=self.file_types)
            if files:
                self.selected_files = list(files)
                self.status_label.config(
                    text=f"{len(files)} file{'s' if len(files) > 1 else ''} selected",
                )
                if self.on_select:
                    self.on_select(self.selected_files)
        else:
            file = filedialog.askopenfilename(filetypes=self.file_types)
            if file:
                self.selected_file = file
                self.status_label.config(
                    text=os.path.basename(file),
                )
                if self.on_select:
                    self.on_select(self.selected_file)

    def get_files(self) -> List[str]:
        """Get selected files (for multiple selection)."""
        return self.selected_files

    def get_file(self) -> Optional[str]:
        """Get selected file (for single selection)."""
        return self.selected_file

    def has_selection(self) -> bool:
        """Check if any files are selected."""
        if self.multiple:
            return len(self.selected_files) > 0
        return self.selected_file is not None
