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

    # Column mappings for each extraction type
    MAPPINGS = {
        ExtractionType.STOCK: ColumnMapping(
            pdf_column=7,  # Actual Balance column
            excel_column=6  # Column G (1-based: 7, 0-based: 6)
        ),
        ExtractionType.FREE: ColumnMapping(
            pdf_column=2,  # الوارد (Incoming) column
            excel_column=5  # Column F (1-based: 6, 0-based: 5)
        ),
        ExtractionType.BUY: ColumnMapping(
            pdf_column=2,  # الوارد (Incoming) column
            excel_column=7  # Column H (1-based: 8, 0-based: 7)
        ),
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
        return cls.MAPPINGS[extraction_type].pdf_column

    @classmethod
    def get_excel_column(cls, extraction_type: ExtractionType) -> int:
        """
        Get Excel column index for extraction type.

        Args:
            extraction_type: Type of extraction

        Returns:
            Column index in Excel (0-based)
        """
        return cls.MAPPINGS[extraction_type].excel_column

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
