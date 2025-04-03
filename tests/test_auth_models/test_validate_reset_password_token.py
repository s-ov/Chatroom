import pytest
import time
from itsdangerous import (
    URLSafeTimedSerializer, 
    SignatureExpired, 
    BadSignature,
    )
from flask import current_app
from app import db
from app.auth.models import User  


# @pytest.fixture
# def user(db_session):
#     """Create a test user"""
#     user = User(email="test@example.com", password="securepassword")
#     db_session.add(user)
#     db_session.commit()
#     return user


def test_validate_reset_password_token_valid(user):
    """Test that a valid token returns the correct user"""
    token = user.generate_reset_password_token()
    validated_user = User.validate_reset_password_token(token, user.id)
    assert validated_user is not None
    assert validated_user.id == user.id


def test_validate_reset_password_token_invalid(user):
    """Test that an invalid token returns None"""
    invalid_token = "invalid.token.string"
    validated_user = User.validate_reset_password_token(invalid_token, user.id)
    assert validated_user is None


def test_validate_reset_password_token_wrong_user(user, db_session):
    """Test that a token from one user does not validate for another user"""
    user2 = User(
        email="test2@example.com", 
        password_hash="anotherpassword",
        )
    db_session.add(user2)
    db_session.commit()

    token = user.generate_reset_password_token()
    validated_user = User.validate_reset_password_token(token, user2.id)  

    assert validated_user is None
