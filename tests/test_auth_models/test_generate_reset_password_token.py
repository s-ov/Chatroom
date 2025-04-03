import pytest
from itsdangerous import (
    URLSafeTimedSerializer, 
    BadSignature, 
    SignatureExpired,
    )
from flask import current_app
from app.auth.models import User  


def test_generate_reset_password_token(user):
    """Test that a reset password token is generated"""
    token = user.generate_reset_password_token()
    assert isinstance(token, str)
    assert len(token) > 0  


def test_verify_reset_password_token(user):
    """Test if the generated token can be verified"""
    token = user.generate_reset_password_token()
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    
    try:
        email = serializer.loads(
            token, 
            salt=user.password_hash, 
            max_age=3600,
            ) 
    except (BadSignature, SignatureExpired):
        email = None

    assert email == user.email  


def test_different_users_have_different_tokens(user, db_session):
    """Ensure different users generate different tokens"""
    user = User(
        email="test@example.com", 
        password_hash="securepassword",
        )
    user2 = User(
        email="test2@example.com", 
        password_hash="anotherpassword",
        )
    db_session.add(user2)
    db_session.commit()

    token1 = user.generate_reset_password_token()
    token2 = user2.generate_reset_password_token()

    assert token1 != token2  


def test_expired_reset_password_token(user, monkeypatch):
    """Test that an expired token is not valid"""
    token = user.generate_reset_password_token()
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    import time
    time.sleep(10)  

    try:
        email = serializer.loads(
            token, 
            salt=user.password_hash, 
            max_age=1,
            )  
    except SignatureExpired:
        email = None 

    assert email is None  
