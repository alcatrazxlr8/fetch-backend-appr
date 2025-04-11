from models import Receipt
import math
from datetime import datetime
import json

def calculate_points(receipt: Receipt) -> int: 
	points = 0

	for char in receipt.retailer:
		if char.isalnum():
			points += 1

	# if str(receipt.total[-2:]) == "00":
	if float(receipt.total) % 1 == 0:
		points += 50
		print(points)
		
	if float(receipt.total) % 0.25 == 0:
		points += 25
		print(points)

	points += 5 * (len(receipt.items) // 2)
	print(points)

	for item in receipt.items:
		price = float(item.price)
		if len(item.shortDescription.strip()) % 3 == 0:
			points += math.ceil(price * 0.2)
			print(points)

	# date = receipt.purchaseDate.split("-")
	# if int(date[2]) % 2 == 1:
	# 	points += 6
	# 	print(points)

	date = receipt.purchaseDate
	date = datetime.strptime(date, "%Y-%m-%d").date()
	receiptDay = date.day
	if receiptDay % 2 == 1:
		points += 6
		print(points)

	time = receipt.purchaseTime # time on receipt
	timeLowerBound = "14:00" # our lower boundary str
	timeUpperBound = "16:00" # our upper boundary str

	time = datetime.strptime(time, "%H:%M").time()
	timeLowerBound = datetime.strptime(timeLowerBound, "%H:%M").time()
	timeUpperBound = datetime.strptime(timeUpperBound, "%H:%M").time()

	if (timeLowerBound < time < timeUpperBound):
		points += 10
		print(points)

	return points