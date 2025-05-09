from uuid import uuid4

from app.models import Receipt
from app.points import calculate_points
from app.storage import receipts_db, points_db

def handle_receipt_submission(receipt: Receipt) -> str:

	receipt_id = str(uuid4())
	points = calculate_points(receipt)

	receipts_db[receipt_id] = receipt
	points_db[receipt_id] = points
	
	return receipt_id