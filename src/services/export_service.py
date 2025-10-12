"""Export service - single responsibility: export data to Excel files."""

from typing import List, Tuple
import pandas as pd


class ExportService:
    """Handles exporting data to Excel files."""

    @staticmethod
    def export_unmatched_codes(
        unmatched_codes: List[Tuple[str, str, str, float, str]],
        file_path: str
    ) -> None:
        """
        Export unmatched codes (in PDF but not in Excel) to Excel file.

        Args:
            unmatched_codes: List of (national_code, item_code, name, balance, pdf_filename) tuples
            file_path: Output file path

        Raises:
            Exception: If export fails
        """
        df = pd.DataFrame(unmatched_codes, columns=["National Code", "Item Code", "Item Name", "Balance", "PDF File"])
        df.to_excel(file_path, index=False)

    @staticmethod
    def export_expired_items(
        expired_items: List[Tuple[str, str, str, str, str]],
        file_path: str
    ) -> None:
        """
        Export expired items to Excel file.

        Args:
            expired_items: List of (national_code, item_code, name, expiry_date, pdf_filename) tuples
            file_path: Output file path

        Raises:
            Exception: If export fails
        """
        df = pd.DataFrame(expired_items, columns=["National Code", "Item Code", "Item Name", "Expiry Date", "PDF File"])
        df.to_excel(file_path, index=False)

    @staticmethod
    def export_duplicates(
        duplicates: List[Tuple[str, str, str, str]],
        file_path: str
    ) -> None:
        """
        Export duplicate codes to Excel file.

        Args:
            duplicates: List of (national_code, item_code, name, pdf_filename) tuples - ALL occurrences
            file_path: Output file path

        Raises:
            Exception: If export fails
        """
        df = pd.DataFrame(duplicates, columns=["National Code", "Item Code", "Item Name", "PDF File"])
        df.to_excel(file_path, index=False)

    @staticmethod
    def export_zero_balance_items(
        zero_balance_items: List[Tuple[str, str, str, str]],
        file_path: str
    ) -> None:
        """
        Export zero balance items to Excel file.

        Args:
            zero_balance_items: List of (national_code, item_code, name, pdf_filename) tuples
            file_path: Output file path

        Raises:
            Exception: If export fails
        """
        df = pd.DataFrame(zero_balance_items, columns=["National Code", "Item Code", "Item Name", "PDF File"])
        df.to_excel(file_path, index=False)
