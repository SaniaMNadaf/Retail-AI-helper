import re
import html
import bleach
from typing import Optional


def esc(value) -> str:
    """Escape text before putting it inside HTML."""
    return html.escape(str(value if value is not None else ""), quote=True)


ALLOWED_TAGS = [
    'b', 'i', 'u', 'em', 'strong', 'p', 'br', 'span', 'div',
    'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td'
]
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
}
ALLOWED_STYLES = [
    'color', 'background-color', 'font-size', 'font-weight',
    'text-align', 'margin', 'padding', 'border', 'border-radius',
    'display', 'flex', 'grid', 'gap', 'width', 'height',
    'border-left', 'border-right', 'border-top', 'border-bottom'
]


def sanitize_html(html: str) -> str:
    """Sanitize HTML to prevent XSS attacks."""
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES,
        strip=True
    )


def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Sanitize plain text input."""
    if not text:
        return ""
    # Remove control characters except newlines/tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    # Limit length
    return text[:max_length].strip()


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Check password strength. Returns (is_valid, message)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    import bcrypt
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


def validate_file_upload(file, allowed_types: list[str], max_size_mb: int = 10) -> tuple[bool, str]:
    """Validate uploaded file type and size."""
    if file is None:
        return False, "No file uploaded"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)  # Reset
    
    if size_mb > max_size_mb:
        return False, f"File size ({size_mb:.1f}MB) exceeds limit ({max_size_mb}MB)"
    
    # Check MIME type
    mime_type = getattr(file, 'type', '')
    if mime_type not in allowed_types:
        return False, f"File type '{mime_type}' not allowed. Allowed: {', '.join(allowed_types)}"
    
    return True, "File is valid"


def sanitize_search_query(query: str) -> str:
    """Sanitize search query to prevent injection."""
    if not query:
        return ""
    # Remove special characters that could be used for injection
    query = re.sub(r'[<>\'";&|`$]', '', query)
    return query[:100].strip()