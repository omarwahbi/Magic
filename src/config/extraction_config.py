"""Configuration for extraction types and their column mappings."""

from enum import Enum
from dataclasses import dataclass


class ExtractionType(Enum):
    """Types of extractions supported."""
    STOCK = "Stock"
    FREE = "Free"
    BUY = "Buy"


@dataclass
class ColumnMapping:
    """Column indices for PDF and Excel operations."""
    pdf_column: int  # Column index in PDF table for balance extraction
    excel_column: int  # Column index in Excel for writing results (0-based)


class ExtractionConfig:
    """Configuration for different extraction types."""

    # PDF column mappings (these are fixed based on PDF structure)
    PDF_COLUMNS = {
        ExtractionType.STOCK: 7,  # Actual Balance column
        ExtractionType.FREE: 2,   # الوارد (Incoming) column
        ExtractionType.BUY: 2,    # الوارد (Incoming) column
    }

    @classmethod
    def get_pdf_column(cls, extraction_type: ExtractionType) -> int:
        """
        Get PDF column index for extraction type.

        Args:
            extraction_type: Type of extraction

        Returns:
            Column index in PDF table
        """
        return cls.PDF_COLUMNS[extraction_type]

    @classmethod
    def get_excel_column(cls, extraction_type: ExtractionType) -> int:
        """
        Get Excel column index for extraction type from settings.

        Args:
            extraction_type: Type of extraction

        Returns:
            Column index in Excel (0-based)
        """
        from src.services.settings_manager import SettingsManager
        
        mappings = SettingsManager.get_column_mappings()
        column_letter = mappings.get(extraction_type.value, "A")
        return SettingsManager.column_letter_to_index(column_letter)

    @classmethod
    def from_string(cls, type_str: str) -> ExtractionType:
        """
        Convert string to ExtractionType.

        Args:
            type_str: String representation ("Stock", "Free", or "Buy")

        Returns:
            Corresponding ExtractionType

        Raises:
            ValueError: If type_str is not valid
        """
        for extraction_type in ExtractionType:
            if extraction_type.value == type_str:
                return extraction_type
        raise ValueError(f"Invalid extraction type: {type_str}")

