from fastapi import FastAPI, HTTPException
from uuid import uuid4
from models import Receipt
from storage import receipts_db, points_db
from points import calculate_points

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Fetch Backend Apprenticeship Assessment"}

@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
	id = str(uuid4())
	points = calculate_points(receipt)
	receipts_db[id] = receipt
	points_db[id] = points

	return {"id": id}

@app.get("/receipts/{id}/points")
async def get_points(id: str):
	if id not in receipts_db:
		raise HTTPException(status_code=404, detail="No receipt found for that ID.")
	return {"points": points_db[id]}
