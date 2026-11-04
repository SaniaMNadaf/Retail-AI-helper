from typing import List, Dict, Any
from datetime import datetime
import uuid
import streamlit as st
import logging

from models.scan_record import ScanRecord
from models.product import ProductAnalysis
from services.database_service import save_scan_record

logger = logging.getLogger("aura_sathi.history")

INITIAL_RECORDS: List[Dict[str, Any]] = [
    {
        "id": "scan-1",
        "product_name": "Amul Organic Whole Milk",
        "category": "Dairy & Groceries",
        "timestamp": "Today, 10:24 AM",
        "verdict": "BUY",
        "safety_score": 9,
        "price": "₹75 (Blinkit)",
        "flagged_ingredients": [],
        "who_insight": "Meets WHO calcium and protein benchmarks. No synthetic hormones.",
    },
    {
        "id": "scan-2",
        "product_name": "Johnson's Baby Gentle Shampoo",
        "category": "Baby Care",
        "timestamp": "Yesterday, 03:40 PM",
        "verdict": "THINK",
        "safety_score": 6,
        "price": "₹195 (FirstCry)",
        "flagged_ingredients": ["Cocamidopropyl Betaine", "Fragrance (Parfum)"],
        "who_insight": "Generally safe, but synthetic fragrances may irritate sensitive infant skin.",
    },
    {
        "id": "scan-3",
        "product_name": "Cetaphil Gentle Skin Cleanser",
        "category": "Skincare",
        "timestamp": "Yesterday, 09:30 AM",
        "verdict": "BUY",
        "safety_score": 10,
        "price": "₹450 (Nykaa)",
        "flagged_ingredients": [],
        "who_insight": "Dermatologist tested. Free from parabens, sulfates, and harsh detergents.",
    },
    {
        "id": "scan-4",
        "product_name": "L'Oreal Paris Total Repair 5 Shampoo",
        "category": "Haircare",
        "timestamp": "2 days ago",
        "verdict": "AVOID",
        "safety_score": 4,
        "price": "₹385 (Amazon)",
        "flagged_ingredients": ["Sodium Laureth Sulfate (SLES)", "Dimethicone (Silicones)", "DMDM Hydantoin"],
        "who_insight": "Contains formaldehyde-releasing preservatives and harsh sulfates that strip scalp moisture.",
    },
    {
        "id": "scan-5",
        "product_name": "Mamaearth Milky Soft Baby Face Cream",
        "category": "Baby Care",
        "timestamp": "2 days ago",
        "verdict": "BUY",
        "safety_score": 9,
        "price": "₹299 (Blinkit)",
        "flagged_ingredients": [],
        "who_insight": "MadeSafe certified. Free from mineral oils, parabens, and synthetic dyes.",
    },
    {
        "id": "scan-6",
        "product_name": "Maybelline SuperStay Matte Ink Lipstick",
        "category": "Cosmetics",
        "timestamp": "3 days ago",
        "verdict": "THINK",
        "safety_score": 5,
        "price": "₹650 (Nykaa)",
        "flagged_ingredients": ["Trimethylsiloxysilicate", "Synthetic Fluorphlogopite"],
        "who_insight": "Long-wear formulation contains heavy silicones; ensure thorough oil cleansing after use.",
    },
    {
        "id": "scan-7",
        "product_name": "The Ordinary Niacinamide 10% + Zinc 1%",
        "category": "Skincare",
        "timestamp": "3 days ago",
        "verdict": "BUY",
        "safety_score": 10,
        "price": "₹600 (Nykaa)",
        "flagged_ingredients": [],
        "who_insight": "High-purity niacinamide and zinc PCA regulate sebum production and strengthen skin barrier.",
    },
    {
        "id": "scan-8",
        "product_name": "Head & Shoulders Cool Menthol Anti-Dandruff",
        "category": "Haircare",
        "timestamp": "4 days ago",
        "verdict": "THINK",
        "safety_score": 5,
        "price": "₹340 (Zepto)",
        "flagged_ingredients": ["Sodium Laureth Sulfate", "Methylisothiazolinone"],
        "who_insight": "Effective for dandruff control, but preservative (MIT) can be a contact sensitizer.",
    },
    {
        "id": "scan-9",
        "product_name": "Himalaya Herbals Baby Powder",
        "category": "Baby Care",
        "timestamp": "5 days ago",
        "verdict": "AVOID",
        "safety_score": 3,
        "price": "₹175 (FirstCry)",
        "flagged_ingredients": ["Talc", "Fragrance"],
        "who_insight": "Talc inhalation poses potential respiratory risks for infants according to pediatric safety guidelines.",
    },
    {
        "id": "scan-10",
        "product_name": "Nutella Hazelnut Cocoa Spread",
        "category": "Food & Spreads",
        "timestamp": "5 days ago",
        "verdict": "AVOID",
        "safety_score": 3,
        "price": "₹340 (Amazon)",
        "flagged_ingredients": ["Palm Oil", "Refined Sugar (56%)"],
        "who_insight": "Exceeds daily free-sugar limit by over 240% in two servings.",
    },
]

def get_initial_records() -> List[ScanRecord]:
    """Returns initial pre-loaded scan records for instant dashboard activity."""
    return [ScanRecord(**item) for item in INITIAL_RECORDS]

def add_scan_to_history(analysis: ProductAnalysis, category: str = "Packaged Food") -> ScanRecord:
    """Creates a ScanRecord from a live Gemini ProductAnalysis and adds it to session state."""
    best_price = "₹ N/A"
    if analysis.online_prices:
        p0 = analysis.online_prices[0]
        platform = getattr(p0, "platform", "Store")
        price_val = getattr(p0, "price", "₹")
        best_price = f"{price_val} ({platform})"

    flagged = []
    if "AVOID" in analysis.verdict:
        flagged.append("Health Risk Flagged")
    if analysis.safety_score < 5:
        flagged.append("Low Safety Score")

    record = ScanRecord(
        id=f"scan-{uuid.uuid4().hex[:6]}",
        product_name=analysis.product_name,
        category=category,
        timestamp="Just now",
        verdict=analysis.verdict,
        safety_score=analysis.safety_score,
        price=best_price,
        flagged_ingredients=flagged,
        who_insight=analysis.who_verdict[:80] + ("..." if len(analysis.who_verdict) > 80 else ""),
    )

    if "scan_history" not in st.session_state:
        st.session_state.scan_history = get_initial_records()

    st.session_state.scan_history.insert(0, record)
    
    # Save to database
    try:
        save_scan_record(record, analysis)
    except Exception as e:
        logger.warning(f"Failed to save scan to database: {e}")
    
    logger.info(f"Added scan to history: {record.product_name} ({record.verdict})")
    return record

def compute_dashboard_metrics(records: List[ScanRecord]) -> Dict[str, Any]:
    """Computes real-time KPI metrics from scan records."""
    total_scans = len(records)
    if total_scans == 0:
        return {
            "total_scans": 0,
            "avg_safety": "0.0",
            "alerts_avoided": 0,
            "money_saved": "₹0",
            "buy_count": 0,
            "think_count": 0,
            "avoid_count": 0,
            "safe_percentage": 0,
        }

    avg_safety = sum(r.safety_score for r in records) / total_scans
    buy_count = sum(1 for r in records if r.verdict == "BUY")
    think_count = sum(1 for r in records if r.verdict == "THINK")
    avoid_count = sum(1 for r in records if r.verdict == "AVOID")
    
    # Avoided hazardous products + flagged allergen ingredients
    alerts_avoided = avoid_count + sum(len(r.flagged_ingredients) for r in records)
    safe_percentage = int((buy_count / total_scans) * 100) if total_scans > 0 else 0
    estimated_savings = f"₹{total_scans * 45 + 120}"

    return {
        "total_scans": total_scans,
        "avg_safety": f"{avg_safety:.1f}",
        "alerts_avoided": alerts_avoided,
        "money_saved": estimated_savings,
        "buy_count": buy_count,
        "think_count": think_count,
        "avoid_count": avoid_count,
        "safe_percentage": safe_percentage,
    }
