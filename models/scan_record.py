from pydantic import BaseModel, Field
from typing import List, Literal

class ScanRecord(BaseModel):
    id: str
    product_name: str
    category: str = "Groceries"
    timestamp: str
    verdict: Literal["BUY", "THINK", "AVOID"]
    safety_score: int = Field(ge=1, le=10)
    price: str = "N/A"
    flagged_ingredients: List[str] = Field(default_factory=list)
    who_insight: str = ""
