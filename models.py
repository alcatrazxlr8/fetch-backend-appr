from pydantic import BaseModel, Field
from datetime import date
from typing import List

class Item(BaseModel):
	shortDescription: str = Field(pattern=r'^[\w\s\-]+$')
	price: str = Field(pattern=r'^\d+\.\d{2}$')

class Receipt(BaseModel):
	retailer: str = Field(pattern=r'^[\w\s\-&]+$')
	purchaseDate: date # date
	purchaseTime: str = Field(pattern=r'^(?:[01]\d|2[0-3]):[0-5]\d$') # 24-hour time
	items: List[Item] = Field(min_length=1)
	total: str = Field(pattern=r'^\d+\.\d{2}$')
