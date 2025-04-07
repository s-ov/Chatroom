from flask import (
    render_template_string, url_for, request,
    )
from flask_mailman import EmailMessage

from urllib.parse import urlparse, urljoin

from config import Config
from app.extensions import db

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

RESET_PASSWORD_EMAIL_HTML_CONTENT = """
    <p>Hello,</p>
    <p>You are receiving this email because you requested a password reset for your account.</p>
    <p>
        To reset your password
        <a href="{{ reset_password_url }}">click here</a>.
    </p>
    <p>
        Alternatively, you can paste the following link in your browser's address bar: <br>
        {{ reset_password_url }}
    </p>
    <p>If you have not requested a password reset please contact someone from the development team.</p>
    <p>
        Thank you!
    </p>
"""

  
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
            RESET_PASSWORD_EMAIL_HTML_CONTENT, 
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1]\
        .lower() in Config.ALLOWED_EXTENSIONS


def follow_user(current_user, user_to_follow):
    """Allow the current user to follow another user."""
    if not current_user.is_following(user_to_follow):
        current_user.followed.append(user_to_follow)
        db.session.commit()


def unfollow_user(current_user, user_to_unfollow):
    """Allow the current user to unfollow another user."""
    if current_user.is_following(user_to_unfollow):
        current_user.followed.remove(user_to_unfollow)
        db.session.commit()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https')\
           and ref_url.netloc == test_url.netloc
