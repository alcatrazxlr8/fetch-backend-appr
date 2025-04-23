from pydantic import BaseModel, Field
from datetime import date
from typing import List

class Item(BaseModel):
	shortDescription: str = Field(
		pattern=r'^[\w\s\-]+$', 
		description="The Short Product Description for the item.", 
		examples=["Mountain Dew 12PK"]
		)
	price: str = Field(
		pattern=r'^\d+\.\d{2}$', 
		description="The total price paid for this item.", 
		examples=["6.49"]
		)

class Receipt(BaseModel):
	retailer: str = Field(
		pattern=r'^[\w\s\-&]+$', 
		description="The name of the retailer or store the receipt is from.", 
		examples=["M&M Corner Market"]
		)
	purchaseDate: date = Field(
		description="The date of the purchase printed on the receipt.", 
		examples=["2022-12-21"]
		) # date (YYYY-MM-DD)
	purchaseTime: str = Field(
		pattern=r'^(?:[01]\d|2[0-3]):[0-5]\d$', 
		description="The time of the purchase printed on the receipt. 24-hour time expected.", 
		examples=["13:01"]
		) # 24-hour time
	items: List[Item] = Field(min_length=1)
	total: str = Field(
		pattern=r'^\d+\.\d{2}$', 
		description="The total amount paid on the receipt.", 
		examples=["6.45"]
		)
