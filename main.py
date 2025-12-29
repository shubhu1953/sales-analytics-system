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
)


def money(n: float) -> str:
    return f"{n:,.2f}"


def main():
    # Paths
    data_file = Path("data") / "sales_data.txt"
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "report.txt"

    # -----------------------------
    # Part 1.1: Read sales data
    # -----------------------------
    raw_lines = read_sales_data(str(data_file))

    # -----------------------------
    # Part 1.2: Parse and clean
    # -----------------------------
    transactions = parse_transactions(raw_lines)

    # -----------------------------
    # Part 1.3: Validate and filter
    # -----------------------------
    valid_transactions, invalid_count, summary = validate_and_filter(
        transactions,
        region=None,
        min_amount=None,
        max_amount=None,
    )

    # Required validation output format
    print(f"Total records parsed: {summary['total_input']}")
    print(f"Invalid records removed: {summary['invalid_records']}")
    print(f"Valid records after cleaning: {summary['final_valid']}")

    # -----------------------------
    # Part 2: Data Processing
    # -----------------------------
    total_revenue = calculate_total_revenue(valid_transactions)
    region_stats = region_wise_sales(valid_transactions)
    daily_trend = daily_sales_trend(valid_transactions)
    peak_date, peak_revenue, peak_txn_count = find_peak_sales_day(valid_transactions)
    top_products = top_selling_products(valid_transactions, n=5)
    low_products = low_performing_products(valid_transactions, threshold=10)
    customers = customer_analysis(valid_transactions)

    # Helpful customer rollups
    customer_count = len(customers)
    top_customer_id, top_customer_spent = ("N/A", 0.0)
    if customers:
        top_customer_id, top_customer_spent = max(
            ((cid, info["total_spent"]) for cid, info in customers.items()),
            key=lambda x: x[1],
        )

    # -----------------------------
    # Print a quick console summary
    # -----------------------------
    print("\n--- Part 2 Summary ---")
    print(f"Total Revenue: {money(total_revenue)}")
    print(f"Peak Sales Day: {peak_date} | Revenue: {money(peak_revenue)} | Transactions: {peak_txn_count}")
    print(f"Top Customer: {top_customer_id} | Total Spent: {money(top_customer_spent)}")

    # -----------------------------
    # Write report.txt
    # -----------------------------
    lines = []
    lines.append("SALES ANALYTICS REPORT")
    lines.append("=" * 22)
    lines.append("")
    lines.append("VALIDATION OUTPUT")
    lines.append(f"Total records parsed: {summary['total_input']}")
    lines.append(f"Invalid records removed: {summary['invalid_records']}")
    lines.append(f"Valid records after cleaning: {summary['final_valid']}")
    lines.append("")
    lines.append("PART 2: SALES SUMMARY")
    lines.append(f"Total Revenue: {money(total_revenue)}")
    lines.append("")

    lines.append("Region-wise Sales (sorted by total sales desc):")
    for region, stats in region_stats.items():
        lines.append(
            f"- {region}: total_sales={money(stats['total_sales'])}, "
            f"transactions={stats['transactions']}, "
            f"percentage={stats['percentage']:.2f}%"
        )
    lines.append("")

    lines.append("Daily Sales Trend (sorted by date):")
    for date, stats in daily_trend.items():
        lines.append(
            f"- {date}: revenue={money(stats['revenue'])}, "
            f"transaction_count={stats['transaction_count']}, "
            f"unique_customers={stats['unique_customers']}"
        )
    lines.append("")

    lines.append("Peak Sales Day:")
    lines.append(f"- {peak_date}: revenue={money(peak_revenue)}, transactions={peak_txn_count}")
    lines.append("")

    lines.append("Top Selling Products (by total quantity sold):")
    for name, qty, rev in top_products:
        lines.append(f"- {name}: total_quantity={qty}, total_revenue={money(rev)}")
    lines.append("")

    lines.append("Low Performing Products (quantity < threshold):")
    if low_products:
        for name, qty, rev in low_products:
            lines.append(f"- {name}: total_quantity={qty}, total_revenue={money(rev)}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("Customer Purchase Analysis:")
    lines.append(f"- Unique customers: {customer_count}")
    lines.append(f"- Top customer: {top_customer_id} (total_spent={money(top_customer_spent)})")
    lines.append("")
    lines.append("Top 5 customers by total_spent:")
    top5_customers = sorted(
        ((cid, info["total_spent"], info["purchase_count"], info["average_order_value"]) for cid, info in customers.items()),
        key=lambda x: x[1],
        reverse=True,
    )[:5]
    for cid, spent, count, aov in top5_customers:
        lines.append(f"- {cid}: total_spent={money(spent)}, purchases={count}, avg_order_value={money(aov)}")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
