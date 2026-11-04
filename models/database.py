from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth users
    name = Column(String(100), default="Aarav Sharma")
    age = Column(Integer, default=25)
    height = Column(String(20), default="")
    weight = Column(String(20), default="")
    health = Column(Text, default="None")
    interests = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    scan_records = relationship("ScanRecordDB", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")


class ScanRecordDB(Base):
    __tablename__ = "scan_records"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), default="Groceries")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    verdict = Column(String(20), nullable=False)
    safety_score = Column(Integer, nullable=False)
    price = Column(String(100), default="N/A")
    flagged_ingredients = Column(JSON, default=list)
    who_insight = Column(Text, default="")
    truth_report = Column(Text, default="")
    who_verdict = Column(Text, default="")
    safety_check = Column(Text, default="")
    voice_script = Column(Text, default="")
    online_prices = Column(JSON, default=list)
    
    user = relationship("User", back_populates="scan_records")
    
    __table_args__ = (
        Index("ix_scan_records_user_timestamp", "user_id", "timestamp"),
    )


class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    gemini_model = Column(String(50), default="gemini-2.5-flash")
    temperature = Column(String(20), default="0.2")
    currency = Column(String(10), default="INR")
    priority_platforms = Column(JSON, default=lambda: ["Blinkit", "Amazon India", "Zepto"])
    auto_play_voice = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    safe_score_threshold = Column(Integer, default=7)
    theme = Column(String(20), default="Light Mode")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="settings")