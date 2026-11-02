"""Email notifications. Section 4.5 has no notifications table, so notifications are sent by email.

In development the console email backend prints the email in the terminal.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_notification(user, subject, message):
    """Email a user. A failed email is logged and never blocks the action that triggered it."""
    try:
        send_mail(
            subject=f"WIL Placement System: {subject}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:  # noqa: BLE001 - email failures must not break the request
        logger.exception("Email to %s failed", user.email)
