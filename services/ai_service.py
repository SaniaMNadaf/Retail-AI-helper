import json
import re
from typing import Optional, Dict, Any
from google import genai
from google.genai import types

from config.settings import API_KEY, DEFAULT_GEMINI_MODEL
from models.product import ProductAnalysis
from utils.logging_config import get_logger

logger = get_logger(__name__)

def _get_client() -> genai.Client:
    """Get authenticated Google GenAI client."""
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured in environment or .env file.")
    return genai.Client(api_key=API_KEY)

def analyze_product_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    user_data: Optional[Dict[str, Any]] = None,
    model_name: str = DEFAULT_GEMINI_MODEL,
    priority_platforms: Optional[list[str]] = None,
) -> ProductAnalysis:
    """
    Analyzes a product label/image using Gemini multimodal model
    tailored to the user's digital twin health profile.
    """
    user_data = user_data or {}
    client = _get_client()

    age = user_data.get("age", 25)
    health = user_data.get("health", "None")
    interests = user_data.get("interests", [])
    interests_str = ", ".join(interests) if isinstance(interests, list) else str(interests)

    platforms_str = ", ".join(priority_platforms) if priority_platforms else "Amazon India, Blinkit, Instamart, Zepto"
    prompt = f"""
    You are Aura Sathi, a strict personal AI shopping bodyguard and safety evaluator.
    Analyze this scanned product label/image carefully against the user's profile:
    - User Age: {age} years
    - Allergies & Health Issues: {health}
    - Lifestyle Preferences & Interests: {interests_str or 'None'}

    Provide a rigorous, truthful assessment:
    1. Identify the exact product name and brand.
    2. Provide a truth report on ingredients, nutritional profile, and marketing claims.
    3. Cross-reference with World Health Organization (WHO) dietary benchmarks and guidelines.
    4. Provide realistic online price comparisons in India from these platforms: {platforms_str} (in ₹).
    5. Highlight any safety risks or allergy warnings tailored to the user.
    6. Deliver a punchy one-sentence voice verdict.
    7. Final verdict: 'BUY' (safe & recommended), 'THINK' (consume in moderation / minor caution), or 'AVOID' (unhealthy / allergen risk).
    8. Safety score integer from 1 to 10.
    """

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProductAnalysis,
                temperature=0.2,
            ),
        )
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        raise

    # 1. Primary: Direct parsed schema from SDK
    if hasattr(response, "parsed") and isinstance(response.parsed, ProductAnalysis):
        return response.parsed

    # 2. Secondary fallback: parse raw response text
    raw_text = response.text or ""
    try:
        return ProductAnalysis.model_validate_json(raw_text)
    except Exception as e:
        logger.warning(f"Failed to parse JSON directly, trying regex fallback: {e}")
        # Fallback regex extraction
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            clean_json = match.group().replace(",}", "}").replace(",]", "]")
            try:
                return ProductAnalysis.model_validate_json(clean_json)
            except Exception as e2:
                logger.error(f"Regex fallback also failed: {e2}")
        raise ValueError(f"Failed to parse product analysis from model output: {raw_text[:200]}")
