from fastapi import FastAPI, HTTPException
from app.models.schemas import ExtractRequest, ApiResponse, TokenUsage
from app.services.image_processing import process_document
from app.services.extractor import extract_bill_data
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Bill Extraction API")

from requests.exceptions import RequestException

@app.post("/extract-bill-data", response_model=ApiResponse)
async def extract_bill_data_endpoint(request: ExtractRequest):
    try:
        # Process document (download and convert to images)
        images = process_document(request.document)
        
        # Extract data using LLM
        data, token_usage = extract_bill_data(images)
        
        return ApiResponse(
            is_success=True,
            token_usage=token_usage,
            data=data
        )
    except RequestException as e:
        # Handle download errors (e.g., 404 Not Found, DNS failure)
        raise HTTPException(status_code=400, detail=f"Failed to download document: {str(e)}")
    except Exception as e:
        # In case of error, we might still want to return a structured error or 500
        # The requirements say "If Status code 200 and following valid schema, then true"
        # So for errors we can raise HTTPException
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
