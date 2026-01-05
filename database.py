import sqlite3

conn = sqlite3.connect("orders.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    service_id INTEGER,
    status TEXT
)
""")
conn.commit()

def save_order(order_id, service_id):
    cur.execute(
        "INSERT OR IGNORE INTO orders VALUES (?, ?, ?)",
        (order_id, service_id, "pending")
    )
    conn.commit()

def update_status(order_id, status):
    cur.execute(
        "UPDATE orders SET status=? WHERE order_id=?",
        (status, order_id)
    )
    conn.commit()

def get_active_orders():
    cur.execute(
        "SELECT order_id, service_id FROM orders WHERE status!='completed'"
    )
    return cur.fetchall()

def has_active_order(service_id):
    cur.execute(
        "SELECT COUNT(*) FROM orders WHERE service_id=? AND status!='completed'",
        (service_id,)
    )
    return cur.fetchone()[0] > 0
