from flask import (
    render_template_string, url_for, request,
    )
from flask_mailman import EmailMessage

from urllib.parse import urlparse, urljoin

from config import Config
from app.extensions import db
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
