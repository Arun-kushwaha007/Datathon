import os
import json
import google.generativeai as genai
from typing import List
from PIL import Image
from app.models.schemas import ExtractionData, PageLineItems, BillItem, TokenUsage

# Configure Gemini
# Assuming API key is in environment variable GOOGLE_API_KEY
# If not, we might need to ask user or use a default if available in the env
if "GOOGLE_API_KEY" not in os.environ:
    # Fallback or error handling. For now, assuming it will be set.
    pass

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def extract_bill_data(images: List[Image.Image]) -> tuple[ExtractionData, TokenUsage]:
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = """
    You are an expert data extraction agent. Your task is to extract line item details from the provided bill images.
    
    For each page, identify if it is a "Bill Detail", "Final Bill", or "Pharmacy" page.
    Extract all line items. For each item, extract:
    - item_name: Exactly as mentioned.
    - item_amount: Net amount of the item post discounts.
    - item_rate: Unit rate.
    - item_quantity: Quantity.
    
    Also count the total number of items across all pages.
    
    Output the data in the following JSON format:
    {
        "pagewise_line_items": [
            {
                "page_no": "string (e.g., '1', '2')",
                "page_type": "Bill Detail | Final Bill | Pharmacy",
                "bill_items": [
                    {
                        "item_name": "string",
                        "item_amount": float,
                        "item_rate": float,
                        "item_quantity": float
                    }
                ]
            }
        ],
        "total_item_count": integer
    }
    
    Ensure you do not miss any items and do not double count.
    Return ONLY the valid JSON.
    """
    
    # Prepare content for Gemini
    content = [prompt]
    for img in images:
        content.append(img)
        
    response = model.generate_content(content)
    
    # Parse usage
    # Gemini usage metadata might be different, but we'll try to get it.
    # usage_metadata is available in response.usage_metadata
    
    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    total_tokens = response.usage_metadata.total_token_count
    
    token_usage = TokenUsage(
        total_tokens=total_tokens,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )
    
    # Parse JSON
    try:
        text = response.text
        # Clean up markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        data_dict = json.loads(text)
        extraction_data = ExtractionData(**data_dict)
        return extraction_data, token_usage
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        print(f"Response text: {response.text}")
        raise ValueError("Failed to parse LLM response")

