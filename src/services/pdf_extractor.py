"""PDF extraction service - single responsibility: extract data from PDFs."""

import logging
from typing import List, Dict, Tuple
import pdfplumber

from src.config.extraction_config import ExtractionType, ExtractionConfig
from src.models.extraction_data import ExtractionData
from src.utils.text_cleaner import clean_text, fix_doubled_chars
from src.utils.date_utils import parse_expiry_date, is_expired, format_date
from src.utils.regex_patterns import CODE_PATTERN


class PDFExtractor:
    """Extracts medicine data from PDF files."""

    def __init__(self, extraction_type: ExtractionType):
        """
        Initialize PDF extractor.

        Args:
            extraction_type: Type of extraction (Stock, Free, or Buy)
        """
        self.extraction_type = extraction_type
        self.column_index = ExtractionConfig.get_pdf_column(extraction_type)

    def extract_from_files(self, pdf_files: List[str], progress_callback=None) -> ExtractionData:
        """
        Extract data from multiple PDF files.

        Args:
            pdf_files: List of PDF file paths
            progress_callback: Optional callback function for progress updates

        Returns:
            ExtractionData containing all extracted information
        """
        extraction_data = ExtractionData()
        code_to_items: Dict[str, List] = {}  # Maps national_code -> [(item_code, name), ...]

        for i, pdf_file in enumerate(pdf_files):
            # Call progress callback if provided
            if progress_callback:
                import os
                filename = os.path.basename(pdf_file)
                progress_callback(f"Processing PDF {i+1}/{len(pdf_files)}: {filename}")

            logging.debug(f"Processing PDF {i+1}/{len(pdf_files)}: {pdf_file}")
            self._extract_from_file(pdf_file, extraction_data, code_to_items)

        # Duplicates are detected at the table level in _find_codes_in_table
        return extraction_data

    def _extract_from_file(
        self,
        pdf_file: str,
        extraction_data: ExtractionData,
        code_to_items: Dict[str, List]
    ) -> None:
        """
        Extract data from a single PDF file.

        Args:
            pdf_file: Path to PDF file
            extraction_data: ExtractionData to populate
            code_to_items: Dictionary tracking national_code -> list of items
        """
        import os
        pdf_filename = os.path.basename(pdf_file)

        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                logging.debug(f"-- Processing Page {page_num + 1} --")
                tables = page.extract_tables()

                if not tables:
                    logging.warning(f"No tables found on page {page_num + 1}")
                    continue

                for table_num, table in enumerate(tables):
                    logging.debug(f"- Processing Table {table_num + 1} on Page {page_num + 1} -")
                    if page_num == 0:  # Log only first page
                        logging.debug(f"Raw Table Content: {table}")

                    self._process_table(table, extraction_data, code_to_items, pdf_filename)

    def _process_table(
        self,
        table: List[List[str]],
        extraction_data: ExtractionData,
        code_to_items: Dict[str, List],
        pdf_filename: str = ""
    ) -> None:
        """
        Process a single table from PDF.

        Args:
            table: Table data as list of rows
            extraction_data: ExtractionData to populate
            code_to_items: Dictionary mapping national_code -> list of items
            pdf_filename: Name of the PDF file being processed
        """
        # Find all codes and their positions
        code_positions = self._find_codes_in_table(table, code_to_items, extraction_data, pdf_filename)

        # Process each position to extract balance and check expiry
        for idx, (row_idx, national_code, item_code, name) in enumerate(code_positions):
            # Skip national code header rows (no item code)
            if not item_code:
                continue

            start_row = row_idx
            end_row = code_positions[idx + 1][0] if idx + 1 < len(code_positions) else len(table)

            logging.debug(f"Processing national code '{national_code}', item '{item_code}'. Row range: {start_row} to {end_row - 1}")

            # Check if item is expired
            if self._is_item_expired(table, start_row, end_row, national_code, item_code, name, extraction_data, pdf_filename):
                continue

            # Extract balance
            self._extract_balance(table, row_idx, end_row, national_code, item_code, name, extraction_data, pdf_filename)

    def _extract_national_and_item_code(self, row: List[str]) -> tuple:
        """
        Extract national code and item code from table row.

        National code format: XX-XXX-XXX (found anywhere in row, doubled)
        Item code format: 4-7 digits (in column 10, NOT doubled)

        Args:
            row: Table row data

        Returns:
            Tuple of (national_code, item_code, is_national_code_row, name)
        """
        import re

        # Match original logic: concatenate all cells and search for code pattern
        # Convert None to empty string to match original behavior
        full_row_text = "".join(str(cell) if cell else "" for cell in row)
        text_no_spaces = re.sub(r'\s+', '', full_row_text)
        text_std_dashes = text_no_spaces.replace('–', '-').replace('—', '-')
        cleaned_text = fix_doubled_chars(text_std_dashes)

        # Search for national code pattern XX-XXX-XXX anywhere in the row
        code_match = re.search(r'([A-Z0-9]{2}-[A-Z0-9]{3}-+[A-Z0-9]{3})', cleaned_text, re.IGNORECASE)

        if code_match:
            national_code = code_match.group(1).upper()
            # Extract name (text before the code in concatenated string)
            name = fix_doubled_chars(full_row_text.split(code_match.group(0))[0].strip())

            # Also try to get name from column 4 (common in Free/Buy PDFs)
            if not name and len(row) > 4 and row[4]:
                name = fix_doubled_chars(str(row[4]).strip())

            logging.debug(f"Found national code: {national_code}, name: {name}")

            # Check if this row also has an item code in column 6 or 10
            item_code = ""
            # Try column 6 first (Free/Buy PDFs)
            if len(row) > 6 and row[6]:
                col6_raw = str(row[6]).strip()
                if re.match(r'^\d{4,7}$', col6_raw):
                    item_code = col6_raw
                    logging.debug(f"  Found item code in col 6: {item_code}")
            # Then try column 10 (Stock PDFs)
            elif len(row) > 10 and row[10]:
                col10_raw = str(row[10]).strip()
                if re.match(r'^\d{4,7}$', col10_raw):
                    item_code = col10_raw
                    logging.debug(f"  Found item code in col 10: {item_code}")

            if item_code:
                return (national_code, item_code, False, name)  # Row with both code and item

            return (national_code, "", True, name)  # National code row only

        # If no national code, check for item code only (item under previous national code)
        # Try column 6 first (Free/Buy PDFs)
        if len(row) > 6 and row[6]:
            col6_raw = str(row[6]).strip()
            if re.match(r'^\d{4,7}$', col6_raw):
                item_code = col6_raw
                # Get name from column 4
                name = ""
                if len(row) > 4 and row[4]:
                    name = fix_doubled_chars(str(row[4]).strip())
                logging.debug(f"Found item code in col 6: {item_code}, name: {name}")
                return ("", item_code, False, name)

        # Then try column 10 (Stock PDFs)
        if len(row) > 10 and row[10]:
            col10_raw = str(row[10]).strip()
            if re.match(r'^\d{4,7}$', col10_raw):
                item_code = col10_raw
                # Get name from column 8
                name = ""
                if len(row) > 8 and row[8]:
                    name = fix_doubled_chars(row[8].strip())
                logging.debug(f"Found item code in col 10: {item_code}, name: {name}")
                return ("", item_code, False, name)

        return ("", "", False, "")

    def _find_codes_in_table(
        self,
        table: List[List[str]],
        code_to_items: Dict[str, List],
        extraction_data: ExtractionData,
        pdf_filename: str = ""
    ) -> List[Tuple[int, str, str, str]]:
        """
        Find all national codes and their items in table.

        Structure:
        - Row with national code in col9+col10 (e.g., "04-A00-021")
        - Following rows have item codes in col10 for that national code
        - Next national code row starts a new group

        Args:
            table: Table data
            code_to_items: Dictionary mapping national_code -> list of (item_code, name)
            extraction_data: For recording items and duplicates

        Returns:
            List of (row_index, national_code, item_code, name) tuples for balance extraction
        """
        positions_for_balance = []
        current_national_code = ""
        national_codes_in_this_table = []  # Track codes within this table

        for r_idx, row in enumerate(table):
            if not row:
                continue

            # Check what type of row this is
            national_code, item_code, is_nat_code_row, name = self._extract_national_and_item_code(row)

            if national_code:
                # Found a national code
                current_national_code = national_code.upper()

                logging.debug(f"Row {r_idx}: National code - {current_national_code}, name: {name}")

                # Check if this code already appeared in THIS table (true duplicate)
                if current_national_code in national_codes_in_this_table:
                    logging.warning(f"DUPLICATE DETECTED: National code {current_national_code} appears multiple times in same table!")

                national_codes_in_this_table.append(current_national_code)

                # Initialize or append items list
                if current_national_code not in code_to_items:
                    code_to_items[current_national_code] = []

                # If this row has both national code AND item code
                if item_code:
                    logging.debug(f"  Row {r_idx} has both national code and item code: {item_code}")
                    code_to_items[current_national_code].append((item_code, name))
                    positions_for_balance.append((r_idx, current_national_code, item_code, name))
                else:
                    # National code only row
                    positions_for_balance.append((r_idx, current_national_code, "", name))

            elif item_code and current_national_code:
                # This is an item row under the current national code
                logging.debug(f"Row {r_idx}: Item {item_code} under national code {current_national_code}, name: {name}")

                # Add this item to the national code's item list
                code_to_items[current_national_code].append((item_code, name))

                # Track for balance extraction
                positions_for_balance.append((r_idx, current_national_code, item_code, name))

        # Check for duplicates: if same code appears multiple times in this table
        code_counts = {}
        for code in national_codes_in_this_table:
            code_counts[code] = code_counts.get(code, 0) + 1

        for national_code, count in code_counts.items():
            if count > 1:
                # TRUE DUPLICATE: same national code appeared multiple times
                logging.debug(f"DUPLICATE: {national_code} appeared {count} times in this table")
                # Record all items under this duplicate code
                if national_code in code_to_items:
                    for item_code, name in code_to_items[national_code]:
                        extraction_data.add_duplicate(national_code, item_code, name, pdf_filename)

        return positions_for_balance

    def _is_item_expired(
        self,
        table: List[List[str]],
        start_row: int,
        end_row: int,
        national_code: str,
        item_code: str,
        name: str,
        extraction_data: ExtractionData,
        pdf_filename: str = ""
    ) -> bool:
        """
        Check if item is expired by scanning rows for expiry date.

        Args:
            table: Table data
            start_row: Start of item rows
            end_row: End of item rows
            national_code: National code (XX-XXX-XXX)
            item_code: Item code (4-7 digits)
            name: Item name
            extraction_data: For recording expired items
            pdf_filename: Name of the PDF file being processed

        Returns:
            True if item is expired, False otherwise
        """
        # Expiry is in column 0 of the current row (DOUBLED - need to fix)
        if start_row < len(table) and len(table[start_row]) > 0:
            cell_value = table[start_row][0]
            if cell_value:
                # Apply fix_doubled to the expiry date
                cell_value_fixed = fix_doubled_chars(cell_value.strip())
                logging.debug(f"      Checking expiry for item {item_code}: raw='{cell_value}' fixed='{cell_value_fixed}'")

                date_parts = parse_expiry_date(cell_value_fixed)
                if date_parts:
                    day, month, year = date_parts
                    logging.debug(f"        Expiry parsed: {day}/{month}/{year}")

                    if is_expired(day, month, year):
                        expiry_str = format_date(day, month, year)
                        logging.debug(f"Item {item_code} (national: {national_code}) is EXPIRED with date {expiry_str}. Skipping.")
                        extraction_data.add_expired_item(national_code, item_code, name, expiry_str, pdf_filename)
                        return True
                    else:
                        logging.debug(f"        Item {item_code} is NOT expired")

        return False

    def _extract_balance(
        self,
        table: List[List[str]],
        row_idx: int,
        end_row: int,
        national_code: str,
        item_code: str,
        name: str,
        extraction_data: ExtractionData,
        pdf_filename: str = ""
    ) -> None:
        """
        Extract balance value for an item.

        Args:
            table: Table data
            row_idx: Current row index (item row)
            end_row: Ending row index
            national_code: National code (XX-XXX-XXX)
            item_code: Item code (4-7 digits)
            name: Item name
            extraction_data: For storing balance
            pdf_filename: Name of the PDF file being processed
        """
        # Find the last non-empty row in the item range (matches original logic)
        balance_row_idx = end_row - 1
        while balance_row_idx > row_idx:
            if any(table[balance_row_idx]):  # Check if row has any content
                break
            balance_row_idx -= 1

        if balance_row_idx < len(table):
            balance_row = table[balance_row_idx]
            logging.debug(f"      >>> Found balance row! Content: {balance_row}")

            # Extract from configured column
            if len(balance_row) > self.column_index:
                cell = balance_row[self.column_index]
                if cell:
                    try:
                        balance_str = str(cell).replace(',', '').strip()
                        balance = float(balance_str)
                        logging.debug(f"        >>> Found balance for national '{national_code}' item '{item_code}': {balance}")

                        # Check if balance is zero
                        if balance == 0:
                            logging.debug(f"        >>> Zero balance detected for '{national_code}' item '{item_code}'")
                            extraction_data.add_zero_balance_item(national_code, item_code, name, pdf_filename)

                        extraction_data.add_balance(national_code, balance, item_code, name, pdf_filename)
                    except (ValueError, TypeError):
                        logging.warning(f"        Could not convert '{cell}' to number.")
                else:
                    # Cell is empty - no balance found
                    logging.debug(f"        >>> No balance found (empty cell) for national '{national_code}' item '{item_code}'")
                    extraction_data.add_zero_balance_item(national_code, item_code, name, pdf_filename)
            else:
                logging.warning(f"      Balance row does not have the required column index: {self.column_index}")
                # Row doesn't have the column - report as zero balance
                extraction_data.add_zero_balance_item(national_code, item_code, name, pdf_filename)
