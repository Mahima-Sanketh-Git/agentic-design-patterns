import sqlite3
import random
from datetime import datetime, timedelta

# ── 1. CREATE & SEED products.db ──────────────────────────────────────────────

def create_db(db_path="products.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("""
        CREATE TABLE transactions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id   INTEGER,
            product_name TEXT,
            brand        TEXT,
            category     TEXT,
            color        TEXT,
            action       TEXT,        -- insert | restock | sale | price_update
            qty_delta    INTEGER,     -- + for insert/restock, - for sale, 0 for price_update
            unit_price   REAL,        -- NULL for restock
            notes        TEXT,
            ts           DATETIME
        )
    """)

    brands     = ["Zephyr", "Lumis", "Kova", "Noric", "Peltra"]
    categories = ["Electronics", "Clothing", "Footwear", "Accessories", "Home"]
    colors     = ["Red", "Blue", "Green", "Black", "White", "Yellow", "Pink", "Gray"]
    names = {
        "Electronics": ["Headphones", "Speaker", "Tablet", "Camera", "Watch"],
        "Clothing":    ["Jacket", "T-Shirt", "Hoodie", "Jeans", "Sweater"],
        "Footwear":    ["Sneakers", "Boots", "Sandals", "Loafers", "Heels"],
        "Accessories": ["Bag", "Belt", "Hat", "Scarf", "Gloves"],
        "Home":        ["Lamp", "Cushion", "Vase", "Rug", "Frame"],
    }

    rows = []
    base_date = datetime(2024, 1, 1)

    for pid in range(1, 41):                          # 40 products
        cat    = random.choice(categories)
        pname  = random.choice(names[cat])
        brand  = random.choice(brands)
        color  = random.choice(colors)
        price  = random.randint(10, 300)
        stock  = 0

        for ev in range(random.randint(8, 20)):       # 8-20 events per product
            ts = base_date + timedelta(days=random.randint(0, 365))

            if stock == 0 or ev == 0:
                action    = "insert" if ev == 0 else "restock"
                qty_delta = random.randint(10, 50)
                unit_price = price
                notes     = "initial stock" if ev == 0 else "restock"
                stock    += qty_delta
            else:
                roll = random.random()
                if roll < 0.6 and stock > 0:
                    action     = "sale"
                    qty_delta  = -random.randint(1, min(5, stock))  # ← NEGATIVE
                    unit_price = price
                    notes      = None
                    stock     += qty_delta
                elif roll < 0.75:
                    action     = "restock"
                    qty_delta  = random.randint(5, 30)
                    unit_price = None                                # ← NULL
                    notes      = "scheduled restock"
                    stock     += qty_delta
                else:
                    action     = "price_update"
                    qty_delta  = 0
                    price      = round(price * random.uniform(0.85, 1.15), 2)
                    unit_price = price
                    notes      = "price adjustment"

            rows.append((pid, pname, brand, cat, color, action,
                         qty_delta, unit_price, notes, ts.strftime("%Y-%m-%d %H:%M:%S")))

    cur.executemany("""
        INSERT INTO transactions
            (product_id, product_name, brand, category, color, action,
             qty_delta, unit_price, notes, ts)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, rows)

    conn.commit()
    conn.close()
    print(f"products.db created — {len(rows)} rows inserted")


# ── 2. EXECUTE SQL  ───────────────────────────────────────────────────────────

def exec_sql(sql, db_path="products.db"):
    """Run any SQL and print results as a neat table."""
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    conn.close()

    if not cols:
        print("query executed — no rows returned")
        return

    # column widths
    widths = [max(len(str(c)), max((len(str(r[i])) for r in rows), default=0))
              for i, c in enumerate(cols)]

    sep  = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    head = "| " + " | ".join(str(c).ljust(w) for c, w in zip(cols, widths)) + " |"

    print(sep)
    print(head)
    print(sep)
    for row in rows:
        print("| " + " | ".join(str(v if v is not None else "NULL").ljust(w)
                                 for v, w in zip(row, widths)) + " |")
    print(sep)
    print(f"  {len(rows)} row(s)\n")
    
    return rows


# ── 3. PRACTICE QUERIES ───────────────────────────────────────────────────────

if __name__ == "__main__":

    create_db()          # run once to build products.db

    # --- peek at data ---
    exec_sql("SELECT * FROM transactions LIMIT 10")

    # --- count events by action type ---
    exec_sql("""
        SELECT action, COUNT(*) AS event_count
        FROM transactions
        GROUP BY action
        ORDER BY event_count DESC
    """)

    # --- V1: WRONG — negative total because qty_delta is negative for sales ---
    exec_sql("""
        SELECT color,
               ROUND(SUM(qty_delta * unit_price), 2) AS total_sales
        FROM transactions
        WHERE action = 'sale'
        GROUP BY color
        ORDER BY total_sales DESC
    """)

    # --- V2: FIXED with ABS() ---
    exec_sql("""
        SELECT color,
               ROUND(SUM(ABS(qty_delta) * unit_price), 2) AS total_sales
        FROM transactions
        WHERE action = 'sale'
        GROUP BY color
        ORDER BY total_sales DESC
    """)

    # --- top brands by revenue ---
    exec_sql("""
        SELECT brand,
               ROUND(SUM(ABS(qty_delta) * unit_price), 2) AS revenue
        FROM transactions
        WHERE action = 'sale'
        GROUP BY brand
        ORDER BY revenue DESC
    """)

    # --- current stock per product ---
    exec_sql("""
        SELECT product_name, color, SUM(qty_delta) AS current_stock
        FROM transactions
        GROUP BY product_id, product_name, color
        HAVING current_stock > 0
        ORDER BY current_stock DESC
        LIMIT 10
    """)