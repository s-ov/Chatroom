import pytest
from app.auth.models import User
from werkzeug.security import check_password_hash


def test_set_password():
    user = User(username="testuser", email="test@example.com")
    user.set_password("securepassword")

    assert user.password_hash is not None
    assert check_password_hash(user.password_hash, "securepassword") is True


def test_check_password():
    user = User(username="testuser", email="test@example.com")
    user.set_password("mypassword")

    assert user.check_password("mypassword") is True
    assert user.check_password("wrongpassword") is False
