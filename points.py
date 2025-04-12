from models import Receipt
import math
from datetime import datetime

def calculate_points(receipt: Receipt) -> int: 
	points = 0

	# Rule 1: Alphanum chars in retailer name
	for char in receipt.retailer:
		if char.isalnum():
			points += 1


	# Rule 2: Total amt is a round figure ("35", "35.00")
	if float(receipt.total) % 1 == 0:
		points += 50


	# Rule 3: Total amt is multiple of 0.25
	if float(receipt.total) % 0.25 == 0:
		points += 25


	# Rule 4: 5 points for every 2 items
	points += 5 * (len(receipt.items) // 2)


	# Rule 5: Item description is multiple of 3
	for item in receipt.items:
		price = float(item.price)
		if len(item.shortDescription.strip()) % 3 == 0:
			points += math.ceil(price * 0.2)


	# Rule 6: Purchased on odd day
	date = str(receipt.purchaseDate)
	date = datetime.strptime(date, "%Y-%m-%d").date()
	receiptDay = date.day
	if receiptDay % 2 == 1:
		points += 6


	# Rule 7: Purchased during a certain time window
	time = receipt.purchaseTime # time on receipt
	timeLowerBound = "14:00" # our lower boundary (str)
	timeUpperBound = "16:00" # our upper boundary (str)

	timeLowerBound = datetime.strptime(timeLowerBound, "%H:%M").time()
	timeUpperBound = datetime.strptime(timeUpperBound, "%H:%M").time()
	time = datetime.strptime(time, "%H:%M").time()

	if (timeLowerBound < time < timeUpperBound):
		points += 10

	# Total Points
	return points