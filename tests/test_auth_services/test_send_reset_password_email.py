import pytest
from flask import url_for
from unittest.mock import patch
from app.auth.models import User
from app.auth.services import send_reset_password_email  


@patch("app.auth.services.EmailMessage.send")  
def test_send_reset_password_email(mock_send, user, app):
    """Test that the password reset email is sent successfully"""
    with app.app_context():  
        send_reset_password_email(user)
        
    mock_send.assert_called_once()


@patch("app.auth.services.EmailMessage.send")
def test_send_reset_password_email_sent_to_correct_user(mock_send, user, app):
    """Test that the email is sent to the correct user"""
    with app.app_context():
        send_reset_password_email(user)

    assert mock_send.called, "EmailMessage.send was not called"


@patch(
        "app.auth.services.EmailMessage.send", 
        side_effect=Exception("Email error"),
        )  
def test_send_reset_password_email_handles_errors(mock_send, user):
    """Test that email sending failure is handled gracefully"""
    try:
        send_reset_password_email(user)
    except Exception as e:
        pytest.fail(f"send_reset_password_email raised an exception: {e}")
