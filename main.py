from pathlib import Path

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    daily_sales_trend,
    find_peak_sales_day,
    top_selling_products,
    low_performing_products,
    customer_analysis,
    generate_sales_report,
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data,
)


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        data_file = Path("data/sales_data.txt")

        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data(str(data_file))
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Show filter options
        print("\n[3/10] Filter Options Available:")
        regions = sorted({t["Region"] for t in transactions})
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if choice == "y":
            region = input("Enter region (or leave blank): ").strip() or None
            min_amount = input("Enter minimum amount (or leave blank): ").strip()
            max_amount = input("Enter maximum amount (or leave blank): ").strip()
            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

        # [4/10] Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount,
        )
        print(f"✓ Valid: {summary['final_valid']} | Invalid: {invalid_count}")

        # [5/10] Perform analysis (Part 2)
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        top_selling_products(valid_transactions)
        low_performing_products(valid_transactions)
        customer_analysis(valid_transactions)
        print("✓ Analysis complete")

        # [6/10] Fetch products from API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        total_valid = len(enriched_transactions)
        rate = (enriched_count / total_valid) * 100 if total_valid else 0
        print(f"✓ Enriched {enriched_count}/{total_valid} transactions ({rate:.1f}%)")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        enriched_file = "data/enriched_sales_data.txt"
        save_enriched_data(enriched_transactions, enriched_file)
        print(f"✓ Saved to: {enriched_file}")

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        report_file = "output/sales_report.txt"
        generate_sales_report(valid_transactions, enriched_transactions, report_file)
        print(f"✓ Report saved to: {report_file}")

        # [10/10] Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print("Something went wrong while running the program.")
        print(f"Details: {e}")
        print("Please check your input files and try again.")


if __name__ == "__main__":
    main()
