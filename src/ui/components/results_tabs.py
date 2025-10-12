"""Results tabs component showing extraction results."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from src.ui.widgets.data_tree import DataTreeView
from src.config.settings import AppSettings
from src.models.extraction_data import ExtractionResult


class ResultsTabs(ttk.Notebook):
    """Notebook widget with matched and unmatched results tabs."""

    def __init__(
        self,
        parent: tk.Widget,
        on_export_unmatched: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize results tabs.

        Args:
            parent: Parent widget
            on_export_unmatched: Callback for exporting unmatched codes
        """
        super().__init__(parent, **kwargs)
        self.settings = AppSettings()
        self.on_export_unmatched = on_export_unmatched

        # Tab 1: Matched items
        matched_frame = ttk.Frame(self)
        self.add(matched_frame, text="Matched Items")

        self.matched_tree = DataTreeView(
            matched_frame,
            columns=[
                ("Code", "National Code", 150),
                ("Balance", "Auto-Extracted", 150),
                ("Status", "Status", 100),
                ("Manual", "Manual Entry", 150),
            ],
            height=self.settings.TREE_HEIGHT
        )
        self.matched_tree.pack(fill="both", expand=True)

        # Configure tags for styling
        self.matched_tree.configure_tag("success", background="#d4edda")
        self.matched_tree.configure_tag("missing", background="#f8d7da")



        # Tab 2: Unmatched codes
        unmatched_frame = ttk.Frame(self)
        self.add(unmatched_frame, text="Codes NOT in Excel")

        ttk.Label(
            unmatched_frame,
            text="These codes were found in PDF but don't exist in your Excel file:",
            style="TLabel"
        ).pack(pady=5)

        self.unmatched_tree = DataTreeView(
            unmatched_frame,
            columns=[
                ("NationalCode", "National Code", 120),
                ("ItemCode", "Item Code", 80),
                ("Name", "Item Name", 200),
                ("Balance", "Balance", 80),
                ("PDFFile", "PDF File", 150),
            ],
            height=self.settings.TREE_HEIGHT
        )
        self.unmatched_tree.pack(fill="both", expand=True)

        ttk.Button(
            unmatched_frame,
            text="Export to Excel",
            command=self._export_unmatched,
        ).pack(pady=5)



    def populate(self, result: ExtractionResult, all_excel_codes: set) -> None:
        """
        Populate tabs with extraction results.

        Args:
            result: Extraction result data
            all_excel_codes: All codes from Excel file
        """
        # Clear existing data
        self.matched_tree.clear()
        self.unmatched_tree.clear()

        # Populate matched items (includes both matched and missing)
        for code in all_excel_codes:
            if code in result.matched_codes:
                balance = result.matched_codes[code]
                status = "✓ OK"
                tag = "success"
            else:
                balance = ""
                status = "✗ Missing"
                tag = "missing"

            self.matched_tree.insert((code, balance, status, ""), tags=(tag,))

        # Populate unmatched codes
        for national_code, item_code, name, balance, pdf_filename in result.unmatched_codes:
            self.unmatched_tree.insert((national_code, item_code, name, balance, pdf_filename))

    def get_matched_selection(self) -> Optional[tuple]:
        """
        Get selected item from matched tree.

        Returns:
            Selected item values or None
        """
        selection = self.matched_tree.get_selection()
        if not selection:
            return None
        return self.matched_tree.get_item_values(selection[0])

    def update_matched_item(self, code: str, balance: float) -> None:
        """
        Update a matched item with new balance.

        Args:
            code: Code to update
            balance: New balance value
        """
        # Find and update the item
        for item_id in self.matched_tree.get_children():
            values = self.matched_tree.get_item_values(item_id)
            if values[0] == code:
                self.matched_tree.update_item(
                    item_id,
                    (code, balance, "✓ Manual", ""),
                    tags=("success",)
                )
                break

    def _export_unmatched(self) -> None:
        """Handle export unmatched button click."""
        if not self.unmatched_tree.get_children():
            messagebox.showwarning("Warning", "No unmatched codes to export.")
            return

        if self.on_export_unmatched:
            self.on_export_unmatched()
