import uuid
from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from models.database import User, UserSettings
from utils.validation import hash_password, verify_password, validate_email, validate_password_strength
from services.database_service import get_db_session, init_db
import logging

logger = logging.getLogger("aura_sathi.auth")


def create_user(email: str, password: str, name: str = None) -> Tuple[bool, str, Optional[User]]:
    """
    Create a new user account.
    Returns (success, message, user_object).
    """
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format", None
    
    # Validate password
    is_valid, msg = validate_password_strength(password)
    if not is_valid:
        return False, msg, None
    
    # Check if user exists
    with get_db_session() as session:
        existing = session.query(User).filter(User.email == email).first()
        if existing:
            return False, "Email already registered", None
        
        # Create user
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=hash_password(password),
            name=name or email.split("@")[0].replace(".", " ").title(),
        )
        session.add(user)
        session.flush()
        
        # Create default settings
        settings = UserSettings(
            id=str(uuid.uuid4()),
            user_id=user.id,
        )
        session.add(settings)
        
        logger.info(f"Created new user: {email}")
        return True, "Account created successfully", user


def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[User]]:
    """
    Authenticate user with email and password.
    Returns (success, message, user_object).
    """
    with get_db_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return False, "Invalid email or password", None
        
        if not user.password_hash:
            return False, "This account uses OAuth. Please sign in with Google.", None
        
        if not verify_password(password, user.password_hash):
            return False, "Invalid email or password", None
        
        if not user.is_active:
            return False, "Account is deactivated", None
        
        # Update last login
        user.last_login = datetime.utcnow()
        logger.info(f"User logged in: {email}")
        return True, "Login successful", user


def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    with get_db_session() as session:
        return session.query(User).filter(User.email == email).first()


def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    with get_db_session() as session:
        return session.query(User).filter(User.id == user_id).first()


def update_user_password(user_id: str, new_password: str) -> Tuple[bool, str]:
    """Update user password."""
    is_valid, msg = validate_password_strength(new_password)
    if not is_valid:
        return False, msg
    
    with get_db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"
        
        user.password_hash = hash_password(new_password)
        logger.info(f"Password updated for user: {user.email}")
        return True, "Password updated successfully"


def deactivate_user(user_id: str) -> Tuple[bool, str]:
    """Deactivate user account."""
    with get_db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"
        
        user.is_active = False
        logger.info(f"User deactivated: {user.email}")
        return True, "Account deactivated"


def create_oauth_user(email: str, name: str = None) -> Tuple[bool, str, User]:
    """Create or get OAuth user (no password)."""
    with get_db_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.last_login = datetime.utcnow()
            return True, "Welcome back!", user
        
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=None,  # OAuth user
            name=name or email.split("@")[0].replace(".", " ").title(),
        )
        session.add(user)
        session.flush()
        
        settings = UserSettings(
            id=str(uuid.uuid4()),
            user_id=user.id,
        )
        session.add(settings)
        
        logger.info(f"Created OAuth user: {email}")
        return True, "Account created via OAuth", user