import httpx

from app.core.config import settings


class EmailConfigError(Exception):
    """Raised when RESEND_API_KEY isn't set, so we fail with a clear message
    instead of a confusing HTTP error deep in httpx."""


class EmailSendError(Exception):
    """Raised when Resend accepts the request but reports a failure."""


def send_password_reset_email(to_email: str, reset_link: str) -> None:
    if not settings.resend_api_key:
        raise EmailConfigError(
            "Email sending isn't configured yet. Set RESEND_API_KEY in your environment."
        )

    html_body = f"""
    <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
      <h2 style="color:#1D2440;">Reset your Marginalia password</h2>
      <p>We received a request to reset the password for this account. This link expires in
         {settings.password_reset_token_expire_minutes} minutes.</p>
      <p style="margin: 28px 0;">
        <a href="{reset_link}"
           style="background:#E2A33D; color:#3A2A0A; padding:12px 20px; border-radius:8px;
                  text-decoration:none; font-weight:600;">
          Reset password
        </a>
      </p>
      <p style="color:#666; font-size:13px;">
        If you didn't request this, you can safely ignore this email — your password won't change.
      </p>
      <p style="color:#999; font-size:12px;">If the button doesn't work, copy this link:<br>{reset_link}</p>
    </div>
    """

    response = httpx.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {settings.resend_api_key}"},
        json={
            "from": settings.email_from,
            "to": [to_email],
            "subject": "Reset your Marginalia password",
            "html": html_body,
        },
        timeout=10.0,
    )

    if response.status_code >= 400:
        raise EmailSendError(f"Resend returned {response.status_code}: {response.text}")
