# Receipt Parser API

A FastAPI-based service that processes receipt images using OCR (Optical Character Recognition) to extract structured data from receipts.

## Features

- Image preprocessing for improved OCR accuracy
- Text extraction using Tesseract OCR
- Receipt data parsing including:
  - Merchant name
  - Date
  - Total amount
  - Individual items
  - Tax and tip (when available)

## Prerequisites

- Docker and Docker Compose
- (Optional) Python 3.11+ for local development

## Getting Started

### Running with Docker

1. Clone the repository:

```bash
git clone <repository-url>
cd receipt-parser
```

2. Start the service using Docker Compose:

```bash
docker compose up --build
```

he API will be available at `http://localhost:8000`

### API Usage

#### Parse Receipt Endpoint

**Endpoint**: `POST /parse-receipt`

**Content-Type**: `multipart/form-data`

**Request Body**:
- `file`: Image file (supported formats: JPG, PNG)

**Example using cURL**:

```bash
curl -X POST \
http://localhost:8000/parse-receipt \
-H 'Content-Type: multipart/form-data' \
-F 'file=@/path/to/receipt.jpg'
```

**Sample Response**:

```json
{
  "receipt_data": {
    "merchant_name": "SAMPLE STORE",
    "date": "2024-02-20T00:00:00",
    "total_amount": 25.99,
    "items": [
      {
        "name": "Item 1",
        "quantity": 1.0,
        "price": 15.99,
        "total": 15.99
      },
      {
        "name": "Item 2",
        "quantity": 1.0,
        "price": 10.00,
        "total": 10.00
      }
    ],
    "tax": null,
    "tip": null
  },
  "text": "Raw OCR text output..."
}
```
