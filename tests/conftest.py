import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def mock_streamlit(monkeypatch):
    """Mock streamlit to avoid runtime errors in tests."""
    import streamlit as st
    
    mock_session_state = {}
    
    class MockSessionState(dict):
        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError:
                raise AttributeError(key)
        
        def __setattr__(self, key, value):
            self[key] = value
        
        def get(self, key, default=None):
            return super().get(key, default)
    
    monkeypatch.setattr(st, "session_state", MockSessionState(mock_session_state))
    monkeypatch.setattr(st, "cache_data", lambda *args, **kwargs: lambda f: f)
    monkeypatch.setattr(st, "error", MagicMock())
    monkeypatch.setattr(st, "warning", MagicMock())
    monkeypatch.setattr(st, "info", MagicMock())
    monkeypatch.setattr(st, "success", MagicMock())
    monkeypatch.setattr(st, "toast", MagicMock())
    monkeypatch.setattr(st, "spinner", MagicMock(return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock())))
    monkeypatch.setattr(st, "rerun", MagicMock())
    monkeypatch.setattr(st, "stop", MagicMock())
    monkeypatch.setattr(st, "set_page_config", MagicMock())
    monkeypatch.setattr(st, "markdown", MagicMock())
    monkeypatch.setattr(st, "button", MagicMock(return_value=False))
    monkeypatch.setattr(st, "text_input", MagicMock(return_value=""))
    monkeypatch.setattr(st, "text_area", MagicMock(return_value=""))
    monkeypatch.setattr(st, "selectbox", MagicMock(return_value=""))
    monkeypatch.setattr(st, "multiselect", MagicMock(return_value=[]))
    monkeypatch.setattr(st, "number_input", MagicMock(return_value=25))
    monkeypatch.setattr(st, "slider", MagicMock(return_value=7))
    monkeypatch.setattr(st, "toggle", MagicMock(return_value=True))
    monkeypatch.setattr(st, "columns", MagicMock(return_value=[MagicMock() for _ in range(4)]))
    monkeypatch.setattr(st, "tabs", MagicMock(return_value=[MagicMock(), MagicMock()]))
    monkeypatch.setattr(st, "container", MagicMock(return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock())))
    monkeypatch.setattr(st, "popover", MagicMock(return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock())))
    monkeypatch.setattr(st, "file_uploader", MagicMock(return_value=None))
    monkeypatch.setattr(st, "camera_input", MagicMock(return_value=None))
    monkeypatch.setattr(st, "dataframe", MagicMock())
    monkeypatch.setattr(st, "altair_chart", MagicMock())
    monkeypatch.setattr(st, "progress", MagicMock())
    monkeypatch.setattr(st, "metric", MagicMock())
    monkeypatch.setattr(st, "caption", MagicMock())
    monkeypatch.setattr(st, "sidebar", MagicMock(__enter__=MagicMock(), __exit__=MagicMock()))
    monkeypatch.setattr(st, "download_button", MagicMock())
    monkeypatch.setattr(st, "audio", MagicMock())
    
    return st


@pytest.fixture
def sample_product_analysis():
    from models.product import ProductAnalysis, PriceItem
    return ProductAnalysis(
        product_name="Test Product",
        truth_report="Test report",
        who_verdict="WHO verdict",
        online_prices=[PriceItem(platform="Amazon", price="₹100")],
        safety_check="Safe for consumption",
        voice_script="This product is safe to buy",
        verdict="BUY",
        safety_score=8
    )


@pytest.fixture
def sample_scan_records():
    from models.scan_record import ScanRecord
    return [
        ScanRecord(id="1", product_name="Product A", timestamp="2024-01-01", verdict="BUY", safety_score=9),
        ScanRecord(id="2", product_name="Product B", timestamp="2024-01-02", verdict="THINK", safety_score=5),
        ScanRecord(id="3", product_name="Product C", timestamp="2024-01-03", verdict="AVOID", safety_score=2, flagged_ingredients=["Palm Oil"]),
    ]