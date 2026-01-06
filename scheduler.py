import asyncio
from smm_api import add_order, check_status
from database import save_order, update_status, get_active_orders, has_active
from config import ORDERS
from notifier import send_admin

async def ensure_orders():
    for cfg in ORDERS:
        if not has_active(cfg["service_id"]):
            r = add_order(cfg["service_id"], cfg["link"], cfg["quantity"])
            if "order" in r:
                save_order(r["order"], cfg["service_id"])
                await send_admin(
                    f"📦 Yangi zakaz\n🛠 {cfg['name']}\n🆔 {r['order']}"
                )

async def check_orders():
    for order_id, service_id in get_active_orders():
        r = check_status(order_id)
        if r.get("status") == "completed":
            update_status(order_id, "completed")
            name = next(o["name"] for o in ORDERS if o["service_id"] == service_id)
            await send_admin(
                f"✅ Bajarildi\n🛠 {name}\n🆔 {order_id}"
            )

async def scheduler_loop():
    while True:
        await ensure_orders()
        await check_orders()
        await asyncio.sleep(60)
