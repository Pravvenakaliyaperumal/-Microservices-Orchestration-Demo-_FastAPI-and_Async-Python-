# service_b.py
from fastapi import FastAPI
app = FastAPI()

# returns product availability and price
@app.get("/product/{product_id}")
async def get_product(product_id: int):
    # pretend database
    products = {
        1: {"product_id": 1, "name": "Widget", "price": 19.99, "in_stock": True},
        2: {"product_id": 2, "name": "Gadget", "price": 29.99, "in_stock": False},
    }
    return products.get(product_id, {"product_id": product_id, "name": "Unknown", "price": 0.0, "in_stock": False})
