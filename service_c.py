# service_c.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PaymentRequest(BaseModel):
    user_id: int
    product_id: int
    amount: float

@app.post("/pay")
async def pay(req: PaymentRequest):
    # simulate approval logic
    if req.amount <= 0:
        return {"status": "rejected", "reason": "invalid amount"}
    # naive approval
    return {"status": "approved", "transaction_id": f"tx-{req.user_id}-{req.product_id}"}
