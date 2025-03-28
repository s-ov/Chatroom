from flask import render_template_string, url_for
from flask_mailman import EmailMessage

from app.auth.reset_password_email_content import (
    reset_password_email_html_content
)
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

  
def send_reset_password_email(user):
    "Send password reset email"

    logger.debug(
        f"Initiating password reset email process for user ID: {user.id},\
          Email: {user.email}",
        )

    try:
        reset_password_url = url_for(
            "auth.reset_password",
            token=user.generate_reset_password_token(),
            user_id=user.id,
            _external=True,
        )
        logger.debug(
            f"Generated reset password URL: {reset_password_url}",
            )

        email_body = render_template_string(
            reset_password_email_html_content, 
            reset_password_url=reset_password_url,
        )
        logger.debug(
            "Rendered reset password email content successfully.",
            )

        message = EmailMessage(
            subject="Reset your password",
            body=email_body,
            to=[user.email],
        )
        message.content_subtype = "html"

        message.send()
        logger.info(
            f"Password reset email sent successfully to {user.email}",
            )

    except Exception as e:
        logger.error(
            f"Failed to send password reset email to {user.email}: {e}", 
            exc_info=True,
            )
