from dataclasses import dataclass

@dataclass
class SaleRecord:
    transaction_id: str
    date: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: int
    customer_id: str
    region: str

    @property
    def revenue(self):
        return self.quantity * self.unit_price

def _to_int(v):
    try:
        return int(v.replace(",", ""))
    except:
        return None

def parse_and_clean(lines):
    total = invalid = 0
    cleaned = []
    for line in lines[1:]:
        total += 1
        parts = line.split("|")
        if len(parts) != 8:
            invalid += 1
            continue
        tid, d, pid, pname, q, p, cid, r = parts
        if not tid.startswith("T") or not cid or not r:
            invalid += 1
            continue
        q = _to_int(q)
        p = _to_int(p)
        if not q or not p or q <= 0 or p <= 0:
            invalid += 1
            continue
        cleaned.append(SaleRecord(tid, d, pid, pname.replace(",", ""), q, p, cid, r))
    return cleaned, total, invalid, len(cleaned)

def compute_metrics(records):
    total_rev = sum(r.revenue for r in records)
    by_product = {}
    by_region = {}
    for r in records:
        by_product[r.product_name] = by_product.get(r.product_name, 0) + r.revenue
        by_region[r.region] = by_region.get(r.region, 0) + r.revenue
    top_product = max(by_product.items(), key=lambda x: x[1])
    regions = sorted(by_region.items(), key=lambda x: x[1], reverse=True)
    return {
        "total_revenue": total_rev,
        "top_product": top_product,
        "revenue_by_region": regions
    }
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        pname = pname.replace(",", "").strip()

        try:
            quantity = int(qty.replace(",", ""))
            unit_price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            "TransactionID": tid.strip(),
            "Date": date.strip(),
            "ProductID": pid.strip(),
            "ProductName": pname,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": cid.strip(),
            "Region": region.strip()
        })

    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns: (valid_transactions, invalid_count, summary)
    """
    valid = []
    invalid_count = 0

    for t in transactions:
        if (
            t["Quantity"] <= 0 or
            t["UnitPrice"] <= 0 or
            not t["TransactionID"].startswith("T") or
            not t["ProductID"].startswith("P") or
            not t["CustomerID"].startswith("C") or
            not t["Region"]
        ):
            invalid_count += 1
            continue

        amount = t["Quantity"] * t["UnitPrice"]

        if region and t["Region"] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue

        valid.append(t)

    summary = {
        "total_input": len(transactions),
        "invalid_records": invalid_count,
        "filtered_by_region": region,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "final_valid": len(valid)
    }

    print("\nFilter Summary:")
    print(f"Region filter: {region}")
    print(f"Transaction amount range: {min_amount} - {max_amount}")
    print(f"Valid records after filtering: {len(valid)}")

    return valid, invalid_count, summary

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float
    """
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total

def region_wise_sales(transactions):
    """
    Aggregates sales by region.
    Returns dictionary with region statistics.
    """
    region_stats = {}

    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_stats:
            region_stats[region] = {
                "total_sales": 0.0,
                "transactions": 0
            }

        region_stats[region]["total_sales"] += amount
        region_stats[region]["transactions"] += 1

    # Add percentage + sort
    for region in region_stats:
        sales = region_stats[region]["total_sales"]
        region_stats[region]["percentage"] = (
            (sales / total_revenue) * 100 if total_revenue else 0
        )

    return dict(
        sorted(
            region_stats.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns dictionary sorted by date.
    """
    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["unique_customers"].add(t["CustomerID"])

    # Convert set to count
    for d in daily:
        daily[d]["unique_customers"] = len(daily[d]["unique_customers"])

    return dict(sorted(daily.items()))

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns tuple: (date, revenue, transaction_count)
    """
    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "count": 0
            }

        daily[date]["revenue"] += amount
        daily[date]["count"] += 1

    peak_date = max(daily.items(), key=lambda x: x[1]["revenue"])
    return peak_date[0], peak_date[1]["revenue"], peak_date[1]["count"]

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns list of tuples.
    """
    products = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if name not in products:
            products[name] = {
                "qty": 0,
                "revenue": 0.0
            }

        products[name]["qty"] += qty
        products[name]["revenue"] += revenue

    result = [
        (name, v["qty"], v["revenue"])
        for name, v in products.items()
    ]

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low total quantity sold.
    Returns list of tuples.
    """
    products = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if name not in products:
            products[name] = {
                "qty": 0,
                "revenue": 0.0
            }

        products[name]["qty"] += qty
        products[name]["revenue"] += revenue

    result = [
        (name, v["qty"], v["revenue"])
        for name, v in products.items()
        if v["qty"] < threshold
    ]

    result.sort(key=lambda x: x[1])
    return result

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns dictionary of customer statistics.
    """
    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products"].add(t["ProductName"])

    # Final formatting
    for cid in customers:
        customers[cid]["average_order_value"] = (
            customers[cid]["total_spent"] / customers[cid]["purchase_count"]
        )
        customers[cid]["products_bought"] = list(customers[cid]["products"])
        del customers[cid]["products"]

    return customers
