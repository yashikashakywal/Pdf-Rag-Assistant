from datetime import datetime, timedelta, timezone
import hashlib
import secrets

import bcrypt
import jwt

from app.core.config import settings

# bcrypt truncates at 72 bytes; reject longer passwords explicitly rather
# than silently truncating them.
_MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > _MAX_PASSWORD_BYTES:
        raise ValueError(f"Password must be at most {_MAX_PASSWORD_BYTES} bytes long.")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(subject: str) -> str:
    """Create a signed JWT whose `sub` claim is the user's id."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


class InvalidTokenError(Exception):
    pass


def decode_access_token(token: str) -> str:
    """Return the user id (`sub`) encoded in a valid, unexpired token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise InvalidTokenError("Invalid or expired token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Invalid token payload")
    return user_id


def generate_reset_token() -> str:
    """
    The raw token that goes in the emailed link. Only ever exists in the
    email itself and briefly in memory — never stored or logged as-is.
    """
    return secrets.token_urlsafe(32)


def hash_reset_token(raw_token: str) -> str:
    """
    A deterministic hash so we can look the token up by value in the DB.
    (Unlike passwords, reset tokens are already high-entropy random strings,
    so a fast deterministic hash is fine here — no per-user salt needed.)
    """
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def reset_token_expiry() -> datetime:
    """
    Naive UTC datetime (no tzinfo) — matches how SQLite/SQLAlchemy stores and
    returns DateTime columns, so comparisons against datetime.utcnow() later
    don't raise a naive-vs-aware TypeError.
    """
    return datetime.utcnow() + timedelta(minutes=settings.password_reset_token_expire_minutes)
