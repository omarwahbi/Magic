"""Medicine item data model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicineItem:
    """Represents a medicine item extracted from PDF."""

    code: str
    name: str
    balance: Optional[float] = None
    expiry_date: Optional[str] = None
    is_expired: bool = False

    def __post_init__(self):
        """Normalize code to uppercase."""
        self.code = self.code.upper()

    def __hash__(self):
        """Hash based on code for use in sets and dicts."""
        return hash(self.code)

    def __eq__(self, other):
        """Equality based on code."""
        if not isinstance(other, MedicineItem):
            return False
        return self.code == other.code
