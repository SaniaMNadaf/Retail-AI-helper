import csv
import io
from datetime import datetime
from typing import List
from models.scan_record import ScanRecord
from models.user import UserProfile


def generate_audit_csv(records: List[ScanRecord], user_profile: UserProfile = None) -> bytes:
    """Generate comprehensive health audit CSV export."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header section
    writer.writerow(["AURA SATHI - HEALTH AUDIT REPORT"])
    writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    writer.writerow([])
    
    # User Profile section
    if user_profile:
        writer.writerow(["USER PROFILE"])
        writer.writerow(["Field", "Value"])
        writer.writerow(["Name", user_profile.name])
        writer.writerow(["Age", user_profile.age])
        writer.writerow(["Height", user_profile.height])
        writer.writerow(["Weight", user_profile.weight])
        writer.writerow(["Health Issues", user_profile.health])
        writer.writerow(["Interests", ", ".join(user_profile.interests) if user_profile.interests else "None"])
        writer.writerow([])
    
    # Summary Metrics
    total = len(records)
    buy_count = sum(1 for r in records if r.verdict == "BUY")
    think_count = sum(1 for r in records if r.verdict == "THINK")
    avoid_count = sum(1 for r in records if r.verdict == "AVOID")
    avg_safety = sum(r.safety_score for r in records) / total if total > 0 else 0
    safe_pct = int((buy_count / total) * 100) if total > 0 else 0
    
    writer.writerow(["SUMMARY METRICS"])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Scans", total])
    writer.writerow(["BUY (Safe)", buy_count])
    writer.writerow(["THINK (Caution)", think_count])
    writer.writerow(["AVOID (Hazard)", avoid_count])
    writer.writerow(["Average Safety Score", f"{avg_safety:.1f}/10"])
    writer.writerow(["Safe Percentage", f"{safe_pct}%"])
    writer.writerow([])
    
    # Detailed Records
    writer.writerow(["DETAILED SCAN HISTORY"])
    writer.writerow([
        "Date/Time", "Product", "Category", "Verdict", 
        "Safety Score", "Best Price", "Flagged Risks", "WHO Insight"
    ])
    
    for record in records:
        writer.writerow([
            record.timestamp,
            record.product_name,
            record.category,
            record.verdict,
            record.safety_score,
            record.price,
            "; ".join(record.flagged_ingredients) if record.flagged_ingredients else "None",
            record.who_insight or "N/A",
        ])
    
    writer.writerow([])
    
    # Flagged Ingredients Summary
    all_flagged = {}
    for record in records:
        for ingredient in record.flagged_ingredients:
            all_flagged[ingredient] = all_flagged.get(ingredient, 0) + 1
    
    if all_flagged:
        writer.writerow(["FLAGGED INGREDIENTS FREQUENCY"])
        writer.writerow(["Ingredient", "Occurrences"])
        for ingredient, count in sorted(all_flagged.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([ingredient, count])
    
    return output.getvalue().encode("utf-8")