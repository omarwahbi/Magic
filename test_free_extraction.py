"""
Test script to verify FREE type extraction fixes.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.pdf_extractor import PDFExtractor
from src.config.extraction_config import ExtractionType

def test_free_extraction():
    """Test FREE extraction with the provided PDF"""

    pdf_path = r"C:\Users\Omar\Desktop\pdfs\مال\اقراص الشركة العامة اسكان.pdf"

    print("=" * 80)
    print("Testing FREE Type Extraction")
    print("=" * 80)

    # Create extractor for FREE type
    extractor = PDFExtractor(ExtractionType.FREE)

    # Extract data
    print(f"\nExtracting from: {pdf_path}")
    result = extractor.extract_from_files([pdf_path])

    # Test the problematic code 02-K00-002
    print("\n" + "=" * 80)
    print("RESULTS FOR NATIONAL CODE: 02-K00-002 (Mebeverine)")
    print("=" * 80)

    code = "02-K00-002"
    if code in result.balances:
        total = result.balances[code]
        print(f"Total Balance: {total}")
        print(f"Expected: 810.0 (120 + 690)")
        if total == 810.0:
            print("Result: [CORRECT]")
        else:
            print(f"Result: [WRONG] - Got {total} instead of 810.0")
    else:
        print(f"ERROR: Code {code} not found in results!")

    # Check if all items are tracked
    if code in result.all_items:
        items = result.all_items[code]
        print(f"\nItems tracked: {len(items)}")
        for idx, (item_code, name, pdf) in enumerate(items, 1):
            print(f"  {idx}. Item: {item_code}, Name: {name}")

    # Show some other extracted codes
    print("\n" + "=" * 80)
    print("OTHER EXTRACTED CODES (First 10)")
    print("=" * 80)

    for idx, (nat_code, balance) in enumerate(list(result.balances.items())[:10]):
        print(f"{idx+1}. {nat_code}: {balance}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    test_free_extraction()
