from uuid import uuid4
from fastapi import HTTPException
from models import Receipt
from points import calculate_points
from storage import receipts_db, points_db

def handle_receipt_submission(receipt: Receipt) -> str:

	if not receipt.retailer.strip():
		raise HTTPException(status_code=400, detail="Retailer name empty")

	if not receipt.items or not all(item.shortDescription.strip() and item.price for item in receipt.items):
		raise HTTPException(status_code=400, detail="Invalid/missing items")
	
	try:
		float(receipt.total)
		for item in receipt.items:
			float(item.price)
	except ValueError:
		raise HTTPException(status_code=400, detail="Price/Total is not a valid float")
	
	receipt_id = str(uuid4())
	points = calculate_points(receipt)

	receipts_db[receipt_id] = receipt
	points_db[receipt_id] = points
	
	return receipt_id