"""
Test script to verify STOCK type extraction (no regression).
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.pdf_extractor import PDFExtractor
from src.config.extraction_config import ExtractionType

def test_stock_extraction():
    """Test STOCK extraction with الاقراص.pdf"""

    pdf_path = r"C:\Users\Omar\Desktop\pdfs\حسب الرمز الوطني\الاقراص.pdf"

    print("=" * 80)
    print("Testing STOCK Type Extraction")
    print("=" * 80)

    # Create extractor for STOCK type
    extractor = PDFExtractor(ExtractionType.STOCK)

    # Extract data
    print(f"\nExtracting from: {pdf_path}")
    result = extractor.extract_from_files([pdf_path])

    # Test the previously problematic code 10-B00-001
    print("\n" + "=" * 80)
    print("RESULTS FOR NATIONAL CODE: 10-B00-001 (Folic acid)")
    print("=" * 80)

    code = "10-B00-001"
    if code in result.balances:
        total = result.balances[code]
        print(f"Total Balance: {total}")
        print(f"Expected: 1650.0 (150 + 1500, NOT 1800!)")
        if total == 1650.0:
            print("Result: [CORRECT]")
        else:
            print(f"Result: [WRONG] - Got {total} instead of 1650.0")
    else:
        print(f"ERROR: Code {code} not found in results!")

    # Check if all items are tracked
    if code in result.all_items:
        items = result.all_items[code]
        print(f"\nItems tracked: {len(items)}")
        for idx, (item_code, name, pdf) in enumerate(items, 1):
            print(f"  {idx}. Item: {item_code}, Name: {name}")

    # Test cross-page tracking
    print("\n" + "=" * 80)
    print("CROSS-PAGE TRACKING TEST: 03-D00-004")
    print("=" * 80)

    code = "03-D00-004"
    if code in result.balances:
        total = result.balances[code]
        print(f"Total Balance: {total}")

        if code in result.all_items:
            items = result.all_items[code]
            print(f"Items tracked: {len(items)}")
            for idx, (item_code, name, pdf) in enumerate(items, 1):
                print(f"  {idx}. Item: {item_code}, Name: {name}")
                if item_code == "3288":
                    print(f"     [OK] Item 3288 (Histadin) correctly assigned to {code}")

    # Show cross-page warnings (should see legitimate ones)
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Total national codes extracted: {len(result.balances)}")
    print(f"First 10 codes:")
    for idx, (nat_code, balance) in enumerate(list(result.balances.items())[:10]):
        print(f"{idx+1}. {nat_code}: {balance}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    test_stock_extraction()
