import os
import csv
import re
from collections import defaultdict

DATASET_DIR = "dataset"

def read_csv_head(path, n=100):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            rows.append([c.strip() for c in row])
            if i >= n:
                break
    return rows

def infer_type(values):
    types = set()
    for v in values:
        v = v.strip()
        if not v:
            continue
        if re.match(r"^\d+$", v):
            types.add("INT")
        elif re.match(r"^\d+\.\d+$", v):
            types.add("DECIMAL(10,2)")
        elif re.match(r"^\d{4}-\d{2}-\d{2}", v):
            types.add("DATETIME")
        else:
            types.add("VARCHAR(255)")
    if not types:
        return "VARCHAR(255)"
    if "VARCHAR(255)" in types:
        return "VARCHAR(255)"
    if "DATETIME" in types:
        return "DATETIME"
    if "DECIMAL(10,2)" in types:
        return "DECIMAL(10,2)"
    return "INT"

def suggest_mysql_type(col_name, values):
    name_lower = col_name.lower()
    if name_lower.endswith("_id") or "_zip" in name_lower or "_prefix" in name_lower:
        return "VARCHAR(64)"
    if any(k in name_lower for k in ["lat", "lng", "price", "value", "weight", "length", "height", "freight"]):
        return "DECIMAL(12,2)"
    if any(k in name_lower for k in ["date", "timestamp", "time"]):
        return "DATETIME"
    if "score" in name_lower or "qty" in name_lower or "photos" in name_lower or "installments" in name_lower or "lenght" in name_lower or "width" in name_lower:
        return "INT"
    return infer_type(values)

def detect_pk_candidates(header, rows):
    col_idx = {h: i for i, h in enumerate(header)}
    candidates = []
    for col in header:
        name_lower = col.lower()
        if not name_lower.endswith("_id"):
            continue
        idx = col_idx[col]
        vals = [r[idx].strip() for r in rows if idx < len(r) and r[idx].strip()]
        if len(set(vals)) == len(vals):
            candidates.append(col)
    # If order_item_id exists, order_id is not PK (composite key)
    if "order_item_id" in header:
        candidates = [c for c in candidates if c != "order_id"]
    return candidates

def analyze():
    files = sorted([f for f in os.listdir(DATASET_DIR) if f.endswith(".csv")])
    schemas = {}
    primary_keys = {}
    foreign_keys = defaultdict(list)

    print("=" * 90)
    print("  DATASET: Olist Brazilian E-Commerce")
    print(f"  Total Files: {len(files)}")
    print("=" * 90)

    for fname in files:
        path = os.path.join(DATASET_DIR, fname)
        rows = read_csv_head(path, 200)
        if not rows:
            continue
        header = rows[0]
        data = rows[1:]

        table_name = fname.replace(".csv", "")
        columns = []

        for i, col in enumerate(header):
            vals = [r[i] for r in data if i < len(r)]
            dtype = suggest_mysql_type(col, vals)
            nullable = "NOT NULL" if col.endswith("_id") else "NULL"
            columns.append((col, dtype, nullable))

        schemas[table_name] = columns
        pk = detect_pk_candidates(header, data)
        primary_keys[table_name] = pk

        # Detect FK: columns ending with _id
        fk_exclude = []
        # For order_items, order_item_id is part of composite PK
        if "order_item_id" in header:
            fk_exclude.append("order_item_id")
        for col in header:
            if not col.endswith("_id") or col in fk_exclude:
                continue
            ref_table = None
            prefix = col.replace("_id", "")
            if prefix == "customer":
                ref_table = "olist_customers_dataset"
            elif prefix == "product":
                ref_table = "olist_products_dataset"
            elif prefix == "seller":
                ref_table = "olist_sellers_dataset"
            elif prefix == "review":
                ref_table = "olist_order_reviews_dataset"
            if ref_table and ref_table != table_name:
                foreign_keys[table_name].append((col, ref_table, prefix + "_id"))

        # Special handling for order_id
        if "order_id" in header:
            # order_id is FK referencing olist_orders_dataset
            if table_name != "olist_orders_dataset":
                foreign_keys[table_name].append(("order_id", "olist_orders_dataset", "order_id"))

    # --- DISPLAY ---
    print("\n" + "=" * 90)
    print("  MYSQL TABLE STRUCTURES")
    print("=" * 90)

    for fname in files:
        table_name = fname.replace(".csv", "")
        cols = schemas[table_name]
        pk = primary_keys.get(table_name, [])

        print(f"\n{'-' * 90}")
        print(f"  TABLE: {table_name}")
        print(f"{'-' * 90}")
        print(f"  CREATE TABLE {table_name} (")
        col_lines = []
        for col, dtype, nullable in cols:
            line = f"    {col} {dtype} {nullable}"
            col_lines.append(line)
        if pk:
            pk_str = ", ".join(pk)
            col_lines.append(f"    PRIMARY KEY ({pk_str})")
        print(",\n".join(col_lines))
        print("  );")
        print(f"\n  -- Sample: {cols[0][0]} = {schemas[table_name][0][0]}...")

    # --- RELATIONSHIPS ---
    print("\n\n" + "=" * 90)
    print("  TABLE RELATIONSHIPS (Foreign Keys)")
    print("=" * 90)
    for src, targets in foreign_keys.items():
        for col, ref_table, ref_col in targets:
            print(f"\n    {src}.{col}  -->  {ref_table}.{ref_col}")

    # --- ENTITY RELATIONSHIP DIAGRAM ---
    print("\n\n" + "=" * 90)
    print("  ENTITY RELATIONSHIP DIAGRAM")
    print("=" * 90)
    lines = [
        "",
        "    +------------------------------------------+",
        "    |  olist_customers                          |",
        "    |  customer_id (PK)  ----------------------+---+",
        "    |  customer_unique_id                       |   |",
        "    |  zip_code_prefix, city, state             |   |",
        "    +------------------------------------------+   |",
        "                                                   |",
        "    +------------------------------------------+   |",
        "    |  olist_orders                             |   |",
        "    |  order_id (PK)                           |   |",
        "    |  customer_id (FK) -----------------------+---+",
        "    |  order_status                             |",
        "    |  purchase_timestamp, approved_at          |",
        "    |  delivered_carrier, delivered_customer    |",
        "    |  estimated_delivery                       |",
        "    +-----------------------+-------------------+",
        "                            |",
        "    +-----------------------+-------------------+   +----------------------------------+",
        "    |  olist_order_items                         |   |  olist_products                    |",
        "    |  order_id (FK) ----------------------------+   |  product_id (PK)                   |",
        "    |  order_item_id                             |   |  product_category_name (FK) ------+---+",
        "    |  product_id (FK) -------------------------+-->|  product_name_lenght               |   |",
        "    |  seller_id (FK) --------------------+     |   |  product_description_lenght        |   |",
        "    |  shipping_limit_date                |     |   |  product_photos_qty                |   |",
        "    |  price, freight_value               |     |   |  weight_g, length_cm               |   |",
        "    +-------------------------------------+     |   |  height_cm, width_cm               |   |",
        "                                                |   +------------------+----------------+---+   |",
        "    +-------------------------------------+     |                      |                      |",
        "    |  olist_sellers                       |     |   +------------------+----------------+   |",
        "    |  seller_id (PK) ---------------------+-----+   |  product_category_name_translation |   |",
        "    |  seller_zip_code_prefix              |         |  product_category_name (PK) --------+---+",
        "    |  seller_city, seller_state           |         |  product_category_name_english      |",
        "    +-------------------------------------+         +---------------------------------------+",
        "",
        "    +------------------------------------------+",
        "    |  olist_order_payments                    |",
        "    |  order_id (FK) --------------------------+",
        "    |  payment_sequential, payment_type        |",
        "    |  payment_installments, payment_value     |",
        "    +------------------------------------------+",
        "",
        "    +------------------------------------------+",
        "    |  olist_order_reviews                     |",
        "    |  review_id (PK)                          |",
        "    |  order_id (FK) --------------------------+",
        "    |  review_score, review_comment_title      |",
        "    |  review_comment_message, review_creation |",
        "    |  review_answer_timestamp                 |",
        "    +------------------------------------------+",
        "",
        "    +------------------------------------------+",
        "    |  olist_geolocation                       |",
        "    |  geolocation_zip_code_prefix             |",
        "    |  geolocation_lat, geolocation_lng        |",
        "    |  geolocation_city, geolocation_state     |",
        "    +------------------------------------------+",
        "    Note: geolocation maps to customers & sellers via zip_code_prefix",
        "",
    ]
    for line in lines:
        print(line)

    print("=" * 90)
    print("  RELATIONSHIP SUMMARY")
    print("=" * 90)
    print("""
    1. olist_orders.customer_id          --> olist_customers.customer_id
    2. olist_order_items.order_id        --> olist_orders.order_id
    3. olist_order_items.product_id      --> olist_products.product_id
    4. olist_order_items.seller_id       --> olist_sellers.seller_id
    5. olist_order_payments.order_id     --> olist_orders.order_id
    6. olist_order_reviews.order_id      --> olist_orders.order_id
    7. olist_products.category_name      --> product_category_name_translation.category_name
    8. olist_customers.zip_code_prefix   --> olist_geolocation.zip_code_prefix (conceptual)
    9. olist_sellers.zip_code_prefix     --> olist_geolocation.zip_code_prefix (conceptual)
    """)


if __name__ == "__main__":
    analyze()
