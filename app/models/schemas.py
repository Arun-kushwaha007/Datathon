from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class BillItem(BaseModel):
    item_name: str = Field(..., description="Exactly as mentioned in the bill")
    item_amount: float = Field(..., description="Net Amount of the item post discounts as mentioned in the bill")
    item_rate: float = Field(..., description="Exactly as mentioned in the bill")
    item_quantity: float = Field(..., description="Exactly as mentioned in the bill")

class PageLineItems(BaseModel):
    page_no: str
    page_type: Literal["Bill Detail", "Final Bill", "Pharmacy"]
    bill_items: List[BillItem]

class ExtractionData(BaseModel):
    pagewise_line_items: List[PageLineItems]
    total_item_count: int

class TokenUsage(BaseModel):
    total_tokens: int
    input_tokens: int
    output_tokens: int

class ApiResponse(BaseModel):
    is_success: bool
    token_usage: TokenUsage
    data: ExtractionData

class ExtractRequest(BaseModel):
    document: str = Field(..., description="URL of the document to process")
