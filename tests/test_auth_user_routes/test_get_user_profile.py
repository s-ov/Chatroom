import pytest
from flask import url_for
from app import db, create_app
from app.auth.models import User


def test_get_user_profile_redirect_if_not_logged_in(client, user):
    """Test that accessing profile without login redirects to login page."""
    response = client.get(url_for("user.get_user_profile", username="testuser"))
    assert response.status_code == 302 
    assert "login" in response.headers["Location"]
