from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from calculator import calculate_tradeoffs

app = FastAPI(title="DFW Rent Vs Commute API")

#Allow frontend to talk to this API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def home():
    return{"message":"Welcome to DFW Rent vs Commute API!"}
@app.get("/api/tradeoff")
def get_tradeoff(hub_id: int =1, rent_weight: float = 0.5):
    """
    Accepts workplace hub_id and user rent_weight,
    returns ranked neighborhood trade-off scores.
    """
    results = calculate_tradeoffs(target_hub_id=hub_id, rent_weight=rent_weight)
    return {
        "hub_id": hub_id,
        "rent_weight": rent_weight,
        "count": len(results),
        "data": results
    }