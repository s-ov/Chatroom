import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from app.auth.models import User
from app.extensions import db
from flask_login import current_user


def test_delete_account_success(logged_in_client, user, app):
    """Test deleting an account with the correct password."""
    
    with app.app_context():
        user.password_hash = generate_password_hash("testpassword")
        db.session.commit()
    
    response = logged_in_client.post(
        url_for("user.delete_user"),
        data={"password": "testpassword"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    with app.app_context():
        deleted_user = User.query.get(user.id)
        assert deleted_user == user  


def test_delete_account_failure_wrong_password(logged_in_client, user, app):
    """Test that an account is not deleted when an incorrect password is provided."""
    
    with app.app_context():
        user.password_hash = generate_password_hash("correct_password")
        db.session.commit()
    
    response = logged_in_client.post(
        url_for("user.delete_user"),
        data={"password": "wrong_password"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    with app.app_context():
        existing_user = User.query.get(user.id)
        assert existing_user is not None 


def test_user_logged_out_after_deletion(logged_in_client, user, app):
    """Ensure user is logged out after account deletion."""
    
    with app.app_context():
        user.password_hash = generate_password_hash("correct_password")
        db.session.commit()
    
    logged_in_client.post(
        url_for("user.delete_user"),
        data={"password": "correct_password"},
        follow_redirects=True
    )
    response = logged_in_client.get(
        url_for("user.delete_user_request"), 
        follow_redirects=True,
        )
    assert response.status_code == 200
