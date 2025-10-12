"""Issues tabs component showing expired items and duplicates."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

from src.ui.widgets.data_tree import DataTreeView
from src.config.settings import AppSettings
from src.models.extraction_data import ExtractionResult


class IssuesTabs(ttk.Notebook):
    """Notebook widget with expired items and duplicate codes tabs."""

    def __init__(
        self,
        parent: tk.Widget,
        on_export_expired: Optional[Callable] = None,
        on_export_duplicates: Optional[Callable] = None,
        on_export_zero_balance: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize issues tabs.

        Args:
            parent: Parent widget
            on_export_expired: Callback for exporting expired items
            on_export_duplicates: Callback for exporting duplicates
        """
        super().__init__(parent, **kwargs)
        self.settings = AppSettings()
        self.on_export_expired = on_export_expired
        self.on_export_duplicates = on_export_duplicates
        self.on_export_zero_balance = on_export_zero_balance

        # Tab 1: Expired Items
        expired_frame = ttk.Frame(self)
        self.add(expired_frame, text="Expired Items")

        ttk.Label(
            expired_frame,
            text="These items were found in the PDF but were skipped because they are expired:",
        ).pack(pady=5)

        self.expired_tree = DataTreeView(
            expired_frame,
            columns=[
                ("NationalCode", "National Code", 120),
                ("ItemCode", "Item Code", 80),
                ("Name", "Item Name", 200),
                ("Expiry", "Expiry Date", 100),
                ("PDFFile", "PDF File", 150),
            ],
            height=self.settings.TREE_HEIGHT
        )
        self.expired_tree.pack(fill="both", expand=True)

        ttk.Button(
            expired_frame,
            text="Export to Excel",
            command=self._export_expired,
        ).pack(pady=5)

        # Tab 2: Duplicate Codes
        duplicate_frame = ttk.Frame(self)
        self.add(duplicate_frame, text="Duplicate Codes")

        ttk.Label(
            duplicate_frame,
            text="These national codes are assigned to more than one item in the PDF:",
        ).pack(pady=5)

        self.duplicate_tree = DataTreeView(
            duplicate_frame,
            columns=[
                ("NationalCode", "National Code", 120),
                ("ItemCode", "Item Code", 80),
                ("Name", "Item Name", 250),
                ("PDFFile", "PDF File", 150),
            ],
            height=self.settings.TREE_HEIGHT
        )
        self.duplicate_tree.pack(fill="both", expand=True)

        ttk.Button(
            duplicate_frame,
            text="Export to Excel",
            command=self._export_duplicates,
        ).pack(pady=5)

        # Tab 3: Zero Balance Items
        zero_balance_frame = ttk.Frame(self)
        self.add(zero_balance_frame, text="Zero Balance Items")

        ttk.Label(
            zero_balance_frame,
            text="These items were found in the PDF but have zero or no balance:",
        ).pack(pady=5)

        self.zero_balance_tree = DataTreeView(
            zero_balance_frame,
            columns=[
                ("NationalCode", "National Code", 120),
                ("ItemCode", "Item Code", 80),
                ("Name", "Item Name", 250),
                ("PDFFile", "PDF File", 200),
            ],
            height=self.settings.TREE_HEIGHT
        )
        self.zero_balance_tree.pack(fill="both", expand=True)

        ttk.Button(
            zero_balance_frame,
            text="Export to Excel",
            command=self._export_zero_balance,
        ).pack(pady=5)



    def populate(self, result: ExtractionResult) -> None:
        """
        Populate tabs with issues data.

        Args:
            result: Extraction result containing issues
        """
        # Clear existing data
        self.expired_tree.clear()
        self.duplicate_tree.clear()
        self.zero_balance_tree.clear()

        # Populate expired items
        for national_code, item_code, name, expiry_date, pdf_filename in result.expired_items:
            self.expired_tree.insert((national_code, item_code, name, expiry_date, pdf_filename))

        # Populate duplicates
        for national_code, item_code, name, pdf_filename in result.duplicates:
            self.duplicate_tree.insert((national_code, item_code, name, pdf_filename))

        # Populate zero balance items
        for national_code, item_code, name, pdf_filename in result.zero_balance_items:
            self.zero_balance_tree.insert((national_code, item_code, name, pdf_filename))

    def _export_expired(self) -> None:
        """Handle export expired button click."""
        if not self.expired_tree.get_children():
            messagebox.showwarning("Warning", "No expired items to export.")
            return

        if self.on_export_expired:
            self.on_export_expired()

    def _export_duplicates(self) -> None:
        """Handle export duplicates button click."""
        if not self.duplicate_tree.get_children():
            messagebox.showwarning("Warning", "No duplicate codes to export.")
            return

        if self.on_export_duplicates:
            self.on_export_duplicates()

    def _export_zero_balance(self) -> None:
        """Handle export zero balance button click."""
        if not self.zero_balance_tree.get_children():
            messagebox.showwarning("Warning", "No zero balance items to export.")
            return

        if self.on_export_zero_balance:
            self.on_export_zero_balance()
