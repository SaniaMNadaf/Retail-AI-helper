from pydantic import BaseModel, Field
from typing import List, Literal

class PriceItem(BaseModel):
    platform: str = Field(description="Name of the online platform e.g., Amazon, Blinkit, Instamart")
    price: str = Field(description="Price string e.g., ₹199")

class ProductAnalysis(BaseModel):
    product_name: str = Field(description="Detected brand and product name")
    truth_report: str = Field(description="Short factual truth report on the product ingredients and claims")
    who_verdict: str = Field(description="Health standards and guidelines check relative to WHO advice")
    online_prices: List[PriceItem] = Field(description="Estimated or comparative prices across online platforms like Amazon, Blinkit, etc.")
    safety_check: str = Field(description="Risk warnings or suitability check based on user allergies and health")
    voice_script: str = Field(description="Punchy, single-sentence summary verdict suitable for voice readout")
    verdict: Literal["BUY", "THINK", "AVOID"] = Field(description="Final purchase recommendation: BUY, THINK, or AVOID")
    safety_score: int = Field(description="Overall safety score integer from 1 to 10", ge=1, le=10)
