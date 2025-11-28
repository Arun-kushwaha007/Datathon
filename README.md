# Bill Extraction API

This project implements an API to extract line item details from bill images using a Vision Language Model (Google Gemini).

## Features

- Extracts line items, rates, quantities, and amounts from multi-page bills.
- Handles PDF and Image formats.
- Uses Google Gemini 2.0 Flash for high-accuracy extraction.
- Returns data in a structured JSON format.

## Solution Approach

This solution leverages the power of **Google Gemini 2.0 Flash**, a state-of-the-art Vision Language Model (VLM), to perform zero-shot extraction of structured data from bill images.

1.  **Image Processing**: The API accepts a document URL. If it's a PDF, it's converted to images using `pdf2image`.
2.  **VLM Extraction**: The images are sent to Gemini 2.0 Flash with a carefully crafted prompt to identify page types (Bill Detail, Final Bill, Pharmacy) and extract line items, rates, and quantities.
3.  **Structured Output**: The LLM response is parsed into a strict JSON schema using Pydantic, ensuring the output matches the required format exactly.
4.  **Error Handling**: Robust error handling manages download failures and API issues.

## Setup

### Option 1: Docker (Recommended)

The easiest way to run the API is using Docker, which handles all system dependencies (like `poppler`).

1.  **Build the image**
    ```bash
    docker build -t bill-extractor .
    ```
2.  **Run the container**
    ```bash
    docker run -d -p 8000:8000 --env-file .env bill-extractor
    ```

### Option 2: Local Python Setup

1.  **Clone the repository**
2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    _Note: You also need `poppler-utils` installed for PDF processing._
    ```bash
    sudo apt-get install poppler-utils  # On Debian/Ubuntu
    ```
3.  **Environment Variables**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

## Usage

1.  **Start the API server**

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

2.  **Send a request**
    ```bash
    curl -X POST "http://localhost:8000/extract-bill-data" \
         -H "Content-Type: application/json" \
         -d '{"document": "https://example.com/bill.pdf"}'
    ```

## API Endpoint

### `POST /extract-bill-data`

**Request Body:**

```json
{
  "document": "string (URL of the document)"
}
```

**Response:**

```json
{
  "is_success": true,
  "token_usage": {
    "total_tokens": 1000,
    "input_tokens": 800,
    "output_tokens": 200
  },
  "data": {
    "pagewise_line_items": [
      {
        "page_no": "1",
        "page_type": "Bill Detail",
        "bill_items": [
          {
            "item_name": "Item 1",
            "item_amount": 100.0,
            "item_rate": 10.0,
            "item_quantity": 10.0
          }
        ]
      }
    ],
    "total_item_count": 1
  }
}
```
