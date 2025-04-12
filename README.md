# Fetch Backend Apprenticeship Assessment 

## Receipt Processor

A simple web service that processes receipts and calculates reward points based on predefined rules.

This project was built for the Fetch Backend Apprenticeship assessment using Python, FastAPI, and Docker.

## Technical Highlights

- **Input Validation**  
  All request bodies are validated using Pydantic with strict type checking and custom regex to ensure format compliance with the OpenAPI specification.

- **Custom Error Handling**  
  Invalid payloads trigger a custom exception handler that returns a clean `400 Bad Request` response (as mentioned in API spec) with human-readable error messages (e.g. `retailer: string does not match <regex>`), catching and replacing default `422` status responses.

- **Modular Architecture**  
  Business logic for receipt processing, point calculation, and validation is encapsulated in separate service modules, keeping route handlers clean and testable.

- **In-Memory Storage**  
  The app uses Python dictionaries to simulate persistent storage as required, ensuring simplicity and stateless behavior.

## Features

- **```POST```** ```/receipts/process```  
  Accepts a JSON receipt and returns a unique receipt ID.  
Request Body: JSON object containing the receipt.  

**Example cURL request:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/receipts/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}'
```
**Response:** 

```bash
{
  "id": "149b53c6-c940-450b-ba3f-ebbcfec5757a"
}
```  


- **```GET```** ```/receipts/{id}/points```  
  Returns the total number of points awarded to a previously submitted receipt.  

**Example cURL request:**

```bash
  curl -X 'GET' \
  'http://127.0.0.1:8000/receipts/149b53c6-c940-450b-ba3f-ebbcfec5757a/points' \
  -H 'accept: application/json'
  ```

**Response:**

```bash
{ "points": 28 }
```
- **Point** Calculation Rules  
  Points are computed based on receipt content, including retailer name, total, item count, and purchase date/time.

  * One point for every alphanumeric character in the retailer name.
  * 50 points if the total is a round dollar amount with no cents.
  * 25 points if the total is a multiple of `0.25`.
  * 5 points for every two items on the receipt.
  * If the trimmed length of the item description is a multiple of 3, multiply the price by `0.2` and round up to the nearest integer. The result is the number of points earned.
  * 6 points if the day in the purchase date is odd.
  * 10 points if the time of purchase is after 2:00pm and before 4:00pm.

---

## How to Run (With Docker)

### 1. Build the Docker image
```bash
docker build -t fetch-backend-appr .
```
### 2. Run the container
```bash
docker run -p 8000:8000 fetch-backend-appr
```

### 3. Access the API
```bash
http://localhost:8000/docs
```
This opens the interactive Swagger UI where you can test both endpoints.  
You can also use cURL or Postman to make API calls


## How to Run (Locally)

### 1. Install **Python** and ```pip```
if not already installed

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Install dependencies using ```pip```
Navigate to the working directory and then
```bash
pip install -r requirements.txt
```

### 3. Run the app
Options to start the app:

_**Auto-reload**_
```bash
uvicorn app.main:app --reload
```
_**Production style: no auto-reload**_
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

--- 

<br>


# Assessment Requirements

Build a webservice that fulfils the documented API. The API is described below. A formal definition is provided 
in the [api.yml](./api.yml) file. We will use the described API to test your solution.

Provide any instructions required to run your application.

Data does not need to persist when your application stops. It is sufficient to store information in memory. There are too many different database solutions, we will not be installing a database on our system when testing your application.

---
## Summary of API Specification

### Endpoint: Process Receipts

* Path: `/receipts/process`
* Method: `POST`
* Payload: Receipt JSON
```json
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    { "shortDescription": "Gatorade", "price": "2.25" },
    { "shortDescription": "Gatorade", "price": "2.25" },
    { "shortDescription": "Gatorade", "price": "2.25" },
    { "shortDescription": "Gatorade", "price": "2.25" }
  ],
  "total": "9.00"
}
```
* Response: JSON containing an id for the receipt.
```json
{ "points": 32 }
```

Description:

Takes in a JSON receipt (see example in the example directory) and returns a JSON object with an ID generated by your code.

The ID returned is the ID that should be passed into `/receipts/{id}/points` to get the number of points the receipt
was awarded.

How many points should be earned are defined by the rules below.

Reminder: Data does not need to survive an application restart. This is to allow you to use in-memory solutions to track any data generated by this endpoint.