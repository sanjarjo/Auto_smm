from smm_api import add_order, check_status
from database import save_order, update_status, get_active_orders, has_active
from config import ORDERS
from app import send_admin

def ensure_orders():
    for cfg in ORDERS:
        if not has_active(cfg["service_id"]):
            r = add_order(cfg["service_id"], cfg["link"], cfg["quantity"])
            if "order" in r:
                save_order(r["order"], cfg["service_id"])
                send_admin(f"📦 Yangi zakaz\n🛠 {cfg['name']}\n🆔 {r['order']}")

def check_orders():
    for order_id, service_id in get_active_orders():
        r = check_status(order_id)
        status = r.get("status")

        if status == "completed":
            update_status(order_id, "completed")
            name = next(o["name"] for o in ORDERS if o["service_id"] == service_id)
            send_admin(f"✅ Bajarildi\n🛠 {name}\n🆔 {order_id}")

    ensure_orders()
