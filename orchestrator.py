# orchestrator.py
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time

app = FastAPI()

# service endpoints (local)
SERVICE_A = "http://127.0.0.1:8001"  # user
SERVICE_B = "http://127.0.0.1:8002"  # product
SERVICE_C = "http://127.0.0.1:8003"  # payment

class OrderRequest(BaseModel):
    user_id: int
    product_id: int

async def fetch_with_retries(client, method, url, *, json=None, params=None,
                             retries=3, timeout=2.0, backoff_factor=0.5):
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = await client.request(method, url, json=json, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except (httpx.HTTPError, httpx.TimeoutException) as e:
            last_exc = e
            if attempt < retries:
                await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))
            else:
                raise
    raise last_exc

@app.post("/place_order")
async def place_order(order: OrderRequest):
    async with httpx.AsyncClient() as client:
        # Start both reads in parallel (user and product)
        user_task = asyncio.create_task(
            fetch_with_retries(client, "GET", f"{SERVICE_A}/user/{order.user_id}")
        )
        product_task = asyncio.create_task(
            fetch_with_retries(client, "GET", f"{SERVICE_B}/product/{order.product_id}")
        )

        # Wait for both results, but with an overall timeout guard
        try:
            user_info, product_info = await asyncio.wait_for(
                asyncio.gather(user_task, product_task),
                timeout=4.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Upstream service timeout")

        # simple business logic: must be in stock
        if not product_info.get("in_stock"):
            return {"status": "failed", "reason": "product_out_of_stock", "product": product_info}

        # perform payment
        payment_payload = {
            "user_id": order.user_id,
            "product_id": order.product_id,
            "amount": product_info.get("price", 0.0)
        }
        try:
            payment_resp = await fetch_with_retries(client, "POST", f"{SERVICE_C}/pay", json=payment_payload, retries=2, timeout=3.0)
        except Exception as e:
            # On payment failure we could trigger compensating actions. Here we report failure.
            return {"status": "failed", "reason": "payment_failed", "error": str(e)}

        # compose final response
        return {
            "status": "success",
            "user": user_info,
            "product": product_info,
            "payment": payment_resp,
            "order_id": f"order-{int(time.time())}"
        }
