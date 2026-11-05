import sys
from pathlib import Path
from contextlib import contextmanager

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models.database import Base
from services.auth_service import create_user, authenticate_user
from services.history_service import (
    get_initial_records,
    add_scan_to_history,
    compute_dashboard_metrics,
    INITIAL_RECORDS
)
from services.audio_service import generate_voice_bytes
from services.database_service import delete_scan_history
from models.product import ProductAnalysis, PriceItem
from models.scan_record import ScanRecord


class TestAuthService:
    def test_user_id_is_available_after_create_and_authenticate(self, monkeypatch):
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        test_session_factory = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        @contextmanager
        def get_test_db_session():
            session = test_session_factory()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        monkeypatch.setattr("services.auth_service.get_db_session", get_test_db_session)

        try:
            created, _, created_user = create_user(
                "login.regression@example.com",
                "SecurePass123!",
            )
            assert created
            assert created_user is not None
            created_user_id = created_user.id

            authenticated, _, authenticated_user = authenticate_user(
                "login.regression@example.com",
                "SecurePass123!",
            )
            assert authenticated
            assert authenticated_user is not None
            assert authenticated_user.id == created_user_id
        finally:
            engine.dispose()


class TestHistoryService:
    def test_init_session_reloads_history_for_existing_login(self, mock_streamlit):
        from utils.session import init_session_state

        mock_streamlit.session_state["user_id"] = "user-123"
        mock_streamlit.session_state["scan_history"] = get_initial_records()

        with patch("utils.session.init_db"):
            with patch("utils.session.get_scan_history", return_value=[]):
                init_session_state()

        assert mock_streamlit.session_state.scan_history == []
        assert mock_streamlit.session_state.history_user_id == "user-123"

    def test_load_user_session_starts_with_empty_history(self, mock_streamlit):
        from models.user import UserProfile
        from utils.session import load_user_session

        with patch("utils.session.get_user_profile", return_value=UserProfile()):
            with patch("utils.session.get_scan_history", return_value=[]):
                load_user_session("user-123")

        assert mock_streamlit.session_state.scan_history == []

    def test_get_initial_records(self):
        records = get_initial_records()
        assert len(records) == 10
        assert all(isinstance(r, ScanRecord) for r in records)
        assert records[0].product_name == "Amul Organic Whole Milk"
        assert records[1].verdict == "THINK"

    def test_compute_dashboard_metrics_empty(self):
        metrics = compute_dashboard_metrics([])
        assert metrics["total_scans"] == 0
        assert metrics["avg_safety"] == "0.0"
        assert metrics["alerts_avoided"] == 0
        assert metrics["money_saved"] == "₹0"

    def test_compute_dashboard_metrics_with_records(self):
        records = [
            ScanRecord(id="1", product_name="A", timestamp="t", verdict="BUY", safety_score=8),
            ScanRecord(id="2", product_name="B", timestamp="t", verdict="THINK", safety_score=5),
            ScanRecord(id="3", product_name="C", timestamp="t", verdict="AVOID", safety_score=3, flagged_ingredients=["Palm Oil"]),
        ]
        metrics = compute_dashboard_metrics(records)
        assert metrics["total_scans"] == 3
        assert metrics["buy_count"] == 1
        assert metrics["think_count"] == 1
        assert metrics["avoid_count"] == 1
        assert metrics["avg_safety"] == "5.3"
        assert metrics["alerts_avoided"] == 2
        assert metrics["safe_percentage"] == 33

    def test_add_scan_to_history(self):
        analysis = ProductAnalysis(
            product_name="Test Product",
            truth_report="Test",
            who_verdict="WHO test",
            online_prices=[PriceItem(platform="Amazon", price="₹100")],
            safety_check="Safe",
            voice_script="Buy it",
            verdict="BUY",
            safety_score=9
        )
        
        mock_state = MagicMock()
        mock_state.scan_history = []
        mock_state.get.return_value = None
        with patch("streamlit.session_state", mock_state):
            record = add_scan_to_history(analysis)
            assert record.product_name == "Test Product"
            assert record.verdict == "BUY"
            assert record.safety_score == 9

    def test_add_scan_to_history_does_not_seed_sample_records(self):
        analysis = ProductAnalysis(
            product_name="Only Real Scan",
            truth_report="Test",
            who_verdict="WHO test",
            online_prices=[],
            safety_check="Safe",
            voice_script="Buy it",
            verdict="BUY",
            safety_score=9,
        )

        mock_state = MagicMock()
        mock_state.__contains__.return_value = False
        mock_state.get.return_value = None
        with patch("streamlit.session_state", mock_state):
            record = add_scan_to_history(analysis)

        assert mock_state.scan_history == [record]

    def test_delete_scan_history_is_scoped_to_user(self):
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_user = MagicMock()
        mock_user.email = "user@example.com"
        mock_session.query.return_value.filter.return_value.first.return_value = mock_user
        mock_session.query.return_value.filter.return_value.delete.return_value = 2

        with patch("services.database_service.get_db_session", return_value=mock_session):
            deleted = delete_scan_history("user-123")

        assert deleted == 2
        assert mock_session.query.call_count == 2


class TestAudioService:
    @patch("streamlit.cache_data", lambda *args, **kwargs: (lambda f: f))
    def test_generate_voice_bytes_empty(self):
        result = generate_voice_bytes("")
        assert result is None
        
        result = generate_voice_bytes("   ")
        assert result is None

    @patch("streamlit.cache_data", lambda *args, **kwargs: (lambda f: f))
    @patch("services.audio_service.gTTS")
    def test_generate_voice_bytes_success(self, mock_gtts):
        mock_tts = MagicMock()
        mock_gtts.return_value = mock_tts
        mock_fp = MagicMock()
        mock_fp.getvalue.return_value = b"fake_audio_data"
        
        with patch("services.audio_service.io.BytesIO", return_value=mock_fp):
            result = generate_voice_bytes("Hello world")
            assert result == b"fake_audio_data"

    @patch("streamlit.cache_data", lambda *args, **kwargs: (lambda f: f))
    @patch("services.audio_service.gTTS")
    def test_generate_voice_bytes_failure(self, mock_gtts):
        mock_gtts.side_effect = Exception("Network error")
        result = generate_voice_bytes("Hello")
        assert result is None