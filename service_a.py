# service_a.py
from fastapi import FastAPI
app = FastAPI()

# simple user lookup
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": "Alice", "tier": "gold"}
