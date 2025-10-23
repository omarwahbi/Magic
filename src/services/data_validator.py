"""Data validation service - single responsibility: validate and match data."""

from typing import Set, Dict, List, Tuple

from src.models.extraction_data import ExtractionData, ExtractionResult


class DataValidator:
    """Validates and matches extraction data against Excel data."""

    @staticmethod
    def validate_and_match(
        extraction_data: ExtractionData,
        excel_codes: Set[str]
    ) -> ExtractionResult:
        """
        Validate extraction data and match against Excel codes.

        Args:
            extraction_data: Data extracted from PDFs
            excel_codes: Codes found in Excel file

        Returns:
            ExtractionResult with matched, unmatched, and missing codes
        """
        result = ExtractionResult()

        # Copy issues from extraction data
        result.expired_items = extraction_data.expired_items.copy()
        result.duplicates = extraction_data.duplicates.copy()
        result.zero_balance_items = extraction_data.zero_balance_items.copy()

        # Match codes
        for national_code, balance in extraction_data.balances.items():
            if national_code in excel_codes:
                result.matched_codes[national_code] = balance
            else:
                # Code not in Excel - add ALL items for this national code
                items = extraction_data.all_items.get(national_code, [("", "", "")])

                # Create one entry per item (shows all batches)
                for item_code, item_name, pdf_filename in items:
                    result.unmatched_codes.append((national_code, item_code, item_name, balance, pdf_filename))

        # Find missing codes (in Excel but not in PDF)
        for code in excel_codes:
            if code not in extraction_data.balances:
                result.missing_codes.append(code)

        return result

    @staticmethod
    def update_manual_balance(
        extraction_result: ExtractionResult,
        code: str,
        balance: float
    ) -> ExtractionResult:
        """
        Update a balance with manual entry.

        Args:
            extraction_result: Current extraction result
            code: Code to update
            balance: New balance value

        Returns:
            Updated extraction result
        """
        code = code.upper()

        # Add or update in matched codes
        extraction_result.matched_codes[code] = balance

        # Remove from missing codes if present
        if code in extraction_result.missing_codes:
            extraction_result.missing_codes.remove(code)

        return extraction_result

    @staticmethod
    def get_summary_stats(result: ExtractionResult) -> Dict[str, int]:
        """
        Get summary statistics for extraction result.

        Args:
            result: Extraction result

        Returns:
            Dictionary with count statistics
        """
        return {
            'matched': result.matched_count,
            'missing': result.missing_count,
            'unmatched': result.unmatched_count,
            'expired': result.expired_count,
            'duplicates': result.duplicate_count,
            'zero_balance': result.zero_balance_count,
        }
