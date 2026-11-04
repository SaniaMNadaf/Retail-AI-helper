import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from models.user import UserProfile
from models.product import ProductAnalysis, PriceItem
from models.scan_record import ScanRecord


class TestUserProfile:
    def test_default_values(self):
        profile = UserProfile()
        assert profile.name == "Aarav Sharma"
        assert profile.age == 25
        assert profile.height == ""
        assert profile.weight == ""
        assert profile.health == "None"
        assert profile.interests == []

    def test_custom_values(self):
        profile = UserProfile(
            name="John Doe",
            age=30,
            height="180cm",
            weight="75kg",
            health="Peanut allergy",
            interests=["Fitness", "Vegan"]
        )
        assert profile.name == "John Doe"
        assert profile.age == 30
        assert profile.height == "180cm"
        assert profile.weight == "75kg"
        assert profile.health == "Peanut allergy"
        assert profile.interests == ["Fitness", "Vegan"]


class TestPriceItem:
    def test_valid_price_item(self):
        item = PriceItem(platform="Amazon", price="₹199")
        assert item.platform == "Amazon"
        assert item.price == "₹199"


class TestProductAnalysis:
    def test_valid_product_analysis(self):
        analysis = ProductAnalysis(
            product_name="Test Product",
            truth_report="Test report",
            who_verdict="WHO says ok",
            online_prices=[PriceItem(platform="Amazon", price="₹100")],
            safety_check="Safe",
            voice_script="Buy this",
            verdict="BUY",
            safety_score=8
        )
        assert analysis.product_name == "Test Product"
        assert analysis.verdict == "BUY"
        assert analysis.safety_score == 8

    def test_invalid_safety_score(self):
        with pytest.raises(Exception):
            ProductAnalysis(
                product_name="Test",
                truth_report="Test",
                who_verdict="Test",
                online_prices=[],
                safety_check="Test",
                voice_script="Test",
                verdict="BUY",
                safety_score=15
            )


class TestScanRecord:
    def test_valid_scan_record(self):
        record = ScanRecord(
            id="scan-123",
            product_name="Test Product",
            timestamp="2024-01-01",
            verdict="BUY",
            safety_score=9
        )
        assert record.id == "scan-123"
        assert record.verdict == "BUY"
        assert record.safety_score == 9
        assert record.category == "Groceries"
        assert record.flagged_ingredients == []