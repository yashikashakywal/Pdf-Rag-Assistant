import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def _uuid() -> str:
    return uuid.uuid4().hex


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Set when a "forgot password" request is made; cleared once used or
    # once a new request supersedes it. We store a hash of the token (never
    # the raw token) so a leaked database still can't be used to reset accounts.
    reset_token_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, default=None)
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None
    )
