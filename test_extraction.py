"""
Quick test script to verify STOCK extraction fixes.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.pdf_extractor import PDFExtractor
from src.config.extraction_config import ExtractionType

def test_stock_extraction():
    """Test Stock extraction with الاقراص.pdf"""

    pdf_path = r"C:\Users\Omar\Desktop\magic - refractored\الاقراص.pdf"

    print("=" * 80)
    print("Testing STOCK Type Extraction")
    print("=" * 80)

    # Create extractor for STOCK type
    extractor = PDFExtractor(ExtractionType.STOCK)

    # Extract data
    print(f"\nExtracting from: {pdf_path}")
    result = extractor.extract_from_files([pdf_path])

    # Show results for the first item (10-B00-001)
    print("\n" + "=" * 80)
    print("RESULTS FOR NATIONAL CODE: 10-B00-001 (ALLOPURINOL)")
    print("=" * 80)

    code = "10-B00-001"
    if code in result.balances:
        total = result.balances[code]
        print(f"Total Balance: {total}")
        print(f"Expected: 1650.0 (150 + 1500, excluding any expired items)")
        if total == 1650.0:
            print("Match: [CORRECT]")
        else:
            print(f"Match: [WRONG] - Got {total} instead of 1650.0")
    else:
        print(f"ERROR: Code {code} not found in results!")

    # Test the problematic codes
    print("\n" + "=" * 80)
    print("TESTING PROBLEMATIC CROSS-PAGE CODES")
    print("=" * 80)

    problematic_codes = ["03-D00-004", "04-B00-004", "01-AA0-004", "02-K00-002"]
    for code in problematic_codes:
        if code in result.balances:
            print(f"{code}: {result.balances[code]} - [FOUND]")
        else:
            print(f"{code}: [NOT FOUND - ERROR!]")

    # Check zero balance items for correct associations
    print("\n" + "=" * 80)
    print("ZERO BALANCE ITEMS (First 10)")
    print("=" * 80)

    if result.zero_balance_items:
        for idx, item in enumerate(list(result.zero_balance_items)[:10]):
            # zero_balance_items is a set of tuples (national_code, item_code, name, pdf_filename)
            if isinstance(item, tuple):
                nat_code, item_code, name, _ = item
                print(f"{idx+1}. Code: {nat_code}, Item: {item_code}, Name: {name}")
            else:
                print(f"{idx+1}. {item}")
    else:
        print("No zero balance items found")

    # Show all extracted balances
    print("\n" + "=" * 80)
    print("ALL EXTRACTED BALANCES (First 10)")
    print("=" * 80)

    for idx, (nat_code, balance) in enumerate(list(result.balances.items())[:10]):
        print(f"{idx+1}. {nat_code}: {balance}")

    # Show expired items
    if result.expired_items:
        print("\n" + "=" * 80)
        print(f"EXPIRED ITEMS DETECTED: {len(result.expired_items)}")
        print("=" * 80)
        for item in list(result.expired_items)[:5]:
            print(f"  - {item.national_code} / {item.item_code}: {item.name} (Expires: {item.expiry_date})")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING, format='%(message)s')
    test_stock_extraction()
