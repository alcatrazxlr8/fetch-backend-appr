from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
	shortDescription: str = Field(pattern=r'^[\w\s\-]+$')
	price: str = Field(pattern=r'^\d+\.\d{2}$')

class Receipt(BaseModel):
	retailer: str = Field(pattern=r'^[\w\s\-&]+$')
	purchaseDate: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')  # ISO date
	purchaseTime: str = Field(pattern=r'^\d{2}:\d{2}$')      # 24-hour time
	items: List[Item]
	total: str = Field(pattern=r'^\d+\.\d{2}$')
