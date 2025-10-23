"""Data structures for extraction results."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class ExtractionData:
    """Container for extracted balance data from PDFs."""

    # Maps national code -> balance
    balances: Dict[str, float] = field(default_factory=dict)

    # Maps national code -> item code (for unmatched report) - DEPRECATED: use all_items
    item_codes: Dict[str, str] = field(default_factory=dict)

    # Maps national code -> item name (for unmatched report) - DEPRECATED: use all_items
    item_names: Dict[str, str] = field(default_factory=dict)

    # Maps national code -> PDF filename (for unmatched report) - DEPRECATED: use all_items
    pdf_sources: Dict[str, str] = field(default_factory=dict)

    # Maps national code -> list of ALL items (item_code, name, pdf_filename)
    all_items: Dict[str, List[Tuple[str, str, str]]] = field(default_factory=dict)

    # Items with expiry issues: (national_code, item_code, name, expiry_date, pdf_filename)
    expired_items: List[Tuple[str, str, str, str, str]] = field(default_factory=list)

    # Duplicate codes: List of (national_code, item_code, name, pdf_filename) for ALL occurrences
    duplicates: List[Tuple[str, str, str, str]] = field(default_factory=list)

    # Items with zero or no balance: (national_code, item_code, name, pdf_filename)
    zero_balance_items: List[Tuple[str, str, str, str]] = field(default_factory=list)

    def add_balance(self, national_code: str, balance: float, item_code: str = "", item_name: str = "", pdf_filename: str = "") -> None:
        """
        Add or update balance for a code.

        Args:
            national_code: National code (XX-XXX-XXX format)
            balance: Balance value to add
            item_code: Item code (4-6 digits)
            item_name: Item name
            pdf_filename: Name of the PDF file where this was found
        """
        national_code = national_code.upper()
        if national_code in self.balances:
            self.balances[national_code] += balance
        else:
            self.balances[national_code] = balance

        # Store item code, name, and PDF source for reporting (DEPRECATED - kept for compatibility)
        if item_code:
            self.item_codes[national_code] = item_code
        if item_name:
            self.item_names[national_code] = item_name
        if pdf_filename:
            self.pdf_sources[national_code] = pdf_filename

        # Track ALL items for this national code (for detailed reporting)
        if item_code or item_name:
            if national_code not in self.all_items:
                self.all_items[national_code] = []
            item_tuple = (item_code, item_name, pdf_filename)
            # Only add if not already present (avoid duplicates)
            if item_tuple not in self.all_items[national_code]:
                self.all_items[national_code].append(item_tuple)

    def add_expired_item(self, national_code: str, item_code: str, name: str, expiry_date: str, pdf_filename: str = "") -> None:
        """
        Record an expired item.

        Args:
            national_code: National code (XX-XXX-XXX format)
            item_code: Item code (4-6 digits)
            name: Item name
            expiry_date: Expiry date string
            pdf_filename: Name of the PDF file where this item was found
        """
        self.expired_items.append((national_code.upper(), item_code, name, expiry_date, pdf_filename))

    def add_duplicate(self, national_code: str, item_code: str, name: str, pdf_filename: str = "") -> None:
        """
        Record a duplicate code occurrence.

        Each call adds ONE occurrence. Multiple calls for the same national code
        will create multiple entries showing ALL items with that code.

        Args:
            national_code: National code (XX-XXX-XXX format)
            item_code: Item code (4-6 digits)
            name: Item name
            pdf_filename: Name of the PDF file where this item was found
        """
        self.duplicates.append((national_code.upper(), item_code, name, pdf_filename))

    def add_zero_balance_item(self, national_code: str, item_code: str, name: str, pdf_filename: str = "") -> None:
        """
        Record an item with zero or missing balance.

        Args:
            national_code: National code (XX-XXX-XXX format)
            item_code: Item code (4-6 digits)
            name: Item name
            pdf_filename: Name of the PDF file where this item was found
        """
        self.zero_balance_items.append((national_code.upper(), item_code, name, pdf_filename))


@dataclass
class ExtractionResult:
    """Result of matching extraction data with Excel file."""

    # Codes that matched and were found in Excel
    matched_codes: Dict[str, float] = field(default_factory=dict)

    # Codes found in PDF but not in Excel: (national_code, item_code, name, balance, pdf_filename)
    unmatched_codes: List[Tuple[str, str, str, float, str]] = field(default_factory=list)

    # Codes in Excel but not found in PDF
    missing_codes: List[str] = field(default_factory=list)

    # Expired items from extraction: (national_code, item_code, name, expiry_date, pdf_filename)
    expired_items: List[Tuple[str, str, str, str, str]] = field(default_factory=list)

    # Duplicate codes from extraction: (national_code, item_code, name, pdf_filename) - ALL occurrences
    duplicates: List[Tuple[str, str, str, str]] = field(default_factory=list)

    # Items with zero or no balance: (national_code, item_code, name, pdf_filename)
    zero_balance_items: List[Tuple[str, str, str, str]] = field(default_factory=list)

    @property
    def matched_count(self) -> int:
        """Number of successfully matched codes."""
        return len(self.matched_codes)

    @property
    def missing_count(self) -> int:
        """Number of codes in Excel not found in PDF."""
        return len(self.missing_codes)

    @property
    def unmatched_count(self) -> int:
        """Number of codes in PDF not found in Excel."""
        return len(self.unmatched_codes)

    @property
    def expired_count(self) -> int:
        """Number of expired items."""
        return len(self.expired_items)

    @property
    def duplicate_count(self) -> int:
        """Number of duplicate codes."""
        return len(self.duplicates)

    @property
    def zero_balance_count(self) -> int:
        """Number of items with zero balance."""
        return len(self.zero_balance_items)
