# Optional API handler placeholder
import requests

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    Returns list of product dictionaries.
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()

        products = []
        for p in data.get("products", []):
            products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating"),
            })

        print("API fetch successful")
        return products

    except Exception as e:
        print(f"API fetch failed: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info.
    Returns dictionary mapping product IDs to info.
    """
    mapping = {}

    for p in api_products:
        pid = p.get("id")
        if pid is not None:
            mapping[pid] = {
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating"),
            }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transactions with API product data.
    Returns list of enriched transaction dictionaries.
    """
    enriched = []

    for t in transactions:
        record = t.copy()

        # Extract numeric product ID (P101 -> 101)
        try:
            numeric_id = int(t["ProductID"][1:])
        except Exception:
            numeric_id = None

        if numeric_id in product_mapping:
            api_info = product_mapping[numeric_id]
            record["API_Category"] = api_info["category"]
            record["API_Brand"] = api_info["brand"]
            record["API_Rating"] = api_info["rating"]
            record["API_Match"] = True
        else:
            record["API_Category"] = None
            record["API_Brand"] = None
            record["API_Rating"] = None
            record["API_Match"] = False

        enriched.append(record)

    return enriched

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file.
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = []
            for h in headers:
                val = t.get(h)
                row.append("" if val is None else str(val))
            f.write("|".join(row) + "\n")
