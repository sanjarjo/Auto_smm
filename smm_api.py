import requests
from config import SMM_API_URL, SMM_API_KEY

def add_order(service, link, quantity):
    return requests.post(SMM_API_URL, data={
        "key": SMM_API_KEY,
        "action": "add",
        "service": service,
        "link": link,
        "quantity": quantity
    }, timeout=15).json()

def check_status(order_id):
    return requests.post(SMM_API_URL, data={
        "key": SMM_API_KEY,
        "action": "status",
        "order": order_id
    }, timeout=15).json()
