from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import (
    create_access_token,
    generate_reset_token,
    hash_password,
    hash_reset_token,
    reset_token_expiry,
    verify_password,
)
from app.db.database import get_db
from app.db.models import User
from app.models.schemas import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    ResetPasswordRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,
)
from app.services.email import EmailConfigError, EmailSendError, send_password_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])

# Shown regardless of whether the email is actually registered, so an
# attacker can't use this endpoint to discover which emails have accounts.
_GENERIC_FORGOT_PASSWORD_MESSAGE = (
    "If an account exists with that email, we've sent a password reset link."
)


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists.",
        )

    user = User(email=payload.email.lower(), hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email)


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()

    # Always return the same message whether or not the account exists —
    # otherwise this endpoint could be used to check who has an account.
    if user is None:
        return MessageResponse(message=_GENERIC_FORGOT_PASSWORD_MESSAGE)

    raw_token = generate_reset_token()
    user.reset_token_hash = hash_reset_token(raw_token)
    user.reset_token_expires_at = reset_token_expiry()
    db.commit()

    reset_link = f"{settings.frontend_base_url}/reset-password.html?token={raw_token}"

    try:
        send_password_reset_email(user.email, reset_link)
    except EmailConfigError as exc:
        # Surfaced as a real error (not the generic message) because this is
        # an operator-facing setup problem, not something to hide from users.
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except EmailSendError as exc:
        raise HTTPException(
            status_code=502, detail=f"Couldn't send the reset email: {exc}"
        ) from exc

    return MessageResponse(message=_GENERIC_FORGOT_PASSWORD_MESSAGE)


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = hash_reset_token(payload.token)
    user = db.query(User).filter(User.reset_token_hash == token_hash).first()

    if user is None or user.reset_token_expires_at is None:
        raise HTTPException(status_code=400, detail="This reset link is invalid or has already been used.")

    if user.reset_token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="This reset link has expired. Please request a new one.")

    user.hashed_password = hash_password(payload.new_password)
    user.reset_token_hash = None
    user.reset_token_expires_at = None
    db.commit()

    return MessageResponse(message="Your password has been reset. You can now sign in.")
