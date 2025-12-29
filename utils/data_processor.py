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
