from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError

from app.models import Receipt
from app.storage import receipts_db, points_db
from app.services import handle_receipt_submission

app = FastAPI(
	title="Receipt Processor",
	description="A simple receipt processor")


# Landing page
@app.get("/")
def root():
	print ({"message": "Fetch Backend Apprenticeship Assessment"})
	return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


# Receipt Processing Endpoint
@app.post("/receipts/process", summary="Submits a receipt for processing.")
def process_receipt(receipt: Receipt):
	"""
	Submits a receipt for processing.
	"""
	receipt_id = handle_receipt_submission(receipt)
	return {"id": receipt_id}


@app.get("/receipts/{id}/points",
		 summary="Returns the points awarded for the receipt.",
		 responses={
		404: {
			"description": "Receipt not found",
			"content": {
				"application/json": {
					"example": {"detail": "No receipt found"}
				}
			}
		}
	})
def get_points(id: str):
	"""
	Returns the points awarded for the receipt.
	"""
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
		custom_errors.append(f"The receipt is Invalid => {field}: {msg}")
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={
			"code": "BAD_REQUEST",
			"detail": custom_errors
			}
	)