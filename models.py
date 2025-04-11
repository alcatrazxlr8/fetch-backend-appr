from pydantic import BaseModel
from typing import List

class Item(BaseModel):
	shortDescription: str
	price: str

class Receipt(BaseModel):
	retailer: str
	purchaseDate: str # YYYY-MM-DD format
	purchaseTime: str # 24 hr format
	items: List[Item]
	total: str