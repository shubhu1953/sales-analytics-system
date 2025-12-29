from utils.file_handler import read_text_lines, ensure_dir, write_text
from utils.data_processor import parse_and_clean, compute_metrics

def format_money(n: int) -> str:
    return f"{n:,}"

def main():
    data_path = "data/sales_data.txt"
    out_dir = ensure_dir("output")
    out_file = out_dir / "report.txt"

    lines = read_text_lines(data_path)
    records, total, invalid, valid = parse_and_clean(lines)

    metrics = compute_metrics(records)

    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {valid}")

    report = []
    report.append("SALES ANALYTICS REPORT\n")
    report.append(f"Total records parsed: {total}")
    report.append(f"Invalid records removed: {invalid}")
    report.append(f"Valid records after cleaning: {valid}\n")
    report.append(f"Total Revenue: {format_money(metrics['total_revenue'])}")
    report.append(f"Top Product: {metrics['top_product'][0]} ({format_money(metrics['top_product'][1])})")
    report.append("\nRevenue by Region:")
    for region, rev in metrics["revenue_by_region"]:
        report.append(f"- {region}: {format_money(rev)}")

    write_text(out_file, "\n".join(report))

if __name__ == "__main__":
    main()
