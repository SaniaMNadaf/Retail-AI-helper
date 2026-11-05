import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from models.database import Base, User, ScanRecordDB, UserSettings
from models.scan_record import ScanRecord
from models.product import ProductAnalysis, PriceItem
from models.user import UserProfile
import uuid
from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger("aura_sathi.database")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aura_sathi.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def init_db():
    """Initialize database tables and run lightweight migrations for missing columns."""
    Base.metadata.create_all(bind=engine)
    
    # Lightweight migration for SQLite to add missing columns if any
    if "sqlite" in DATABASE_URL:
        try:
            with engine.connect() as conn:
                res = conn.execute(text("PRAGMA table_info(user_settings);"))
                columns = [row[1] for row in res.fetchall()]
                if "theme" not in columns:
                    conn.execute(text("ALTER TABLE user_settings ADD COLUMN theme VARCHAR(20) DEFAULT 'Light Mode';"))
                    conn.commit()
                    logger.info("Migrated database: added theme column to user_settings")
        except Exception as e:
            logger.warning(f"Database migration check failed: {e}")

    logger.info("Database initialized")


@contextmanager
def get_db_session() -> Session:
    """Context manager for database sessions."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    with get_db_session() as session:
        return session.query(User).filter(User.id == user_id).first()


def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    with get_db_session() as session:
        return session.query(User).filter(User.email == email).first()


def create_default_user(session: Session, email: str = "default@aurasathi.ai") -> User:
    """Create default demo user or return existing one."""
    existing = session.query(User).filter(User.email == email).first()
    if existing:
        # Ensure user has settings
        existing_settings = session.query(UserSettings).filter(UserSettings.user_id == existing.id).first()
        if not existing_settings:
            settings = UserSettings(id=str(uuid.uuid4()), user_id=existing.id)
            session.add(settings)
            session.flush()
        return existing

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        name="Aarav Sharma",
        age=28,
        height="178cm",
        weight="72kg",
        health="Lactose sensitivity, Low sodium diet",
        interests=["Fitness", "Organic"],
    )
    session.add(user)
    session.flush()
    
    # Create default settings if not exists
    existing_settings = session.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    if not existing_settings:
        settings = UserSettings(
            id=str(uuid.uuid4()),
            user_id=user.id,
        )
        session.add(settings)
        session.flush()
        
    logger.info(f"Created new user: {user.email}")
    return user


def user_to_profile(user: User) -> UserProfile:
    """Convert DB User to UserProfile model."""
    return UserProfile(
        name=user.name,
        age=user.age,
        height=user.height,
        weight=user.weight,
        health=user.health,
        interests=user.interests or [],
    )


def profile_to_user(profile: UserProfile, user: User):
    """Update DB User from UserProfile model."""
    user.name = profile.name
    user.age = profile.age
    user.height = profile.height
    user.weight = profile.weight
    user.health = profile.health
    user.interests = profile.interests


def scan_record_to_db(record: ScanRecord, user_id: str, analysis: ProductAnalysis = None) -> ScanRecordDB:
    """Convert ScanRecord to DB model."""
    prices = []
    if analysis and analysis.online_prices:
        prices = [{"platform": p.platform, "price": p.price} for p in analysis.online_prices]
    
    return ScanRecordDB(
        id=record.id,
        user_id=user_id,
        product_name=record.product_name,
        category=record.category,
        timestamp=datetime.utcnow(),
        verdict=record.verdict,
        safety_score=record.safety_score,
        price=record.price,
        flagged_ingredients=record.flagged_ingredients,
        who_insight=record.who_insight,
        truth_report=analysis.truth_report if analysis else "",
        who_verdict=analysis.who_verdict if analysis else "",
        safety_check=analysis.safety_check if analysis else "",
        voice_script=analysis.voice_script if analysis else "",
        online_prices=prices,
    )


def db_to_scan_record(db_record: ScanRecordDB) -> ScanRecord:
    """Convert DB ScanRecord to model."""
    return ScanRecord(
        id=db_record.id,
        product_name=db_record.product_name,
        category=db_record.category,
        timestamp=db_record.timestamp.strftime("%Y-%m-%d %H:%M"),
        verdict=db_record.verdict,
        safety_score=db_record.safety_score,
        price=db_record.price,
        flagged_ingredients=db_record.flagged_ingredients or [],
        who_insight=db_record.who_insight,
    )


def save_scan_record(record: ScanRecord, analysis: ProductAnalysis = None, user_id: str = None) -> ScanRecordDB:
    """Save scan record to database."""
    with get_db_session() as session:
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")
        else:
            raise ValueError("user_id required for save_scan_record")
        
        db_record = scan_record_to_db(record, user.id, analysis)
        session.add(db_record)
        session.flush()
        logger.info(f"Saved scan record: {record.product_name} for user {user.email}")
        session.expunge(db_record)
        return db_record


def get_scan_history(user_id: str = None, limit: int = 100) -> List[ScanRecord]:
    """Get user's scan history from database."""
    with get_db_session() as session:
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")
        else:
            raise ValueError("user_id required for get_scan_history")
        
        db_records = session.query(ScanRecordDB)\
            .filter(ScanRecordDB.user_id == user.id)\
            .order_by(ScanRecordDB.timestamp.desc())\
            .limit(limit)\
            .all()
        return [db_to_scan_record(r) for r in db_records]


def get_user_profile(user_id: str = None) -> UserProfile:
    """Get user profile from database."""
    with get_db_session() as session:
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")
        else:
            raise ValueError("user_id required for get_user_profile")
        return user_to_profile(user)


def update_user_profile(profile: UserProfile, user_id: str = None) -> User:
    """Update user profile in database."""
    with get_db_session() as session:
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")
        else:
            raise ValueError("user_id required for update_user_profile")
        
        profile_to_user(profile, user)
        logger.info(f"Updated profile for user: {user.email}")
        session.expunge(user)
        return user


def get_user_settings(user_id: str = None) -> UserSettings:
    """Get user settings from database."""
    with get_db_session() as session:
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")
        else:
            raise ValueError("user_id required for get_user_settings")
        
        # Explicitly query settings to avoid lazy loading issues
        settings = session.query(UserSettings).filter(UserSettings.user_id == user.id).first()
        if not settings:
            settings = UserSettings(id=str(uuid.uuid4()), user_id=user.id)
            session.add(settings)
            session.flush()
        session.expunge(settings)
        return settings


def update_user_settings(settings_data: dict, user_id: str = None) -> UserSettings:
    """Update user settings in database."""
    with get_db_session() as session:
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User not found: {user_id}")
        else:
            raise ValueError("user_id required for update_user_settings")
        
        settings = session.query(UserSettings).filter(UserSettings.user_id == user.id).first()
        if not settings:
            settings = UserSettings(id=str(uuid.uuid4()), user_id=user.id)
            session.add(settings)
            session.flush()
        
        for key, value in settings_data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        session.flush()
        session.expunge(settings)
        logger.info(f"Updated settings for user: {user.email}")
        return settings