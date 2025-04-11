from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from models import Receipt
from storage import receipts_db, points_db
from services import handle_receipt_submission

app = FastAPI()

# Landing page
@app.get("/")
async def root():
	return {"message": "Fetch Backend Apprenticeship Assessment"}

# Receipt Processing Endpoint
@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
	try:
		receipt_id = handle_receipt_submission(receipt)
		return {"id": receipt_id}
	except HTTPException as e:
		raise e

@app.get("/receipts/{id}/points")
async def get_points(id: str):
	if id not in receipts_db:
		raise HTTPException(status_code=404, detail="No receipt found for that ID.")
	return {"points": points_db[id]}

# Catching and overriding the pydantic validation error status
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	errors = exc.errors()
	custom_errors = []
	for error in errors:
		field = ".".join(str(loc) for loc in error["loc"] if isinstance(loc, str) and loc != "body")
		msg = error["msg"]
		custom_errors.append(f"{field}: {msg}")
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": custom_errors}
	)