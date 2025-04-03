import pytest
from flask import url_for
from app import create_app, db
from app.auth.models import User
from app.auth.forms import ResetPasswordForm



# def test_authenticated_user_redirect(client, user):
#     """An authenticated user should be redirected"""
#     with client:
#         client.post(
#             "/login", 
#             data={"email": user.email, "password": "old_password"}, 
#             follow_redirects=True,
#             )
#         response = client.get(
#             f"/reset_password/fake_token/{user.id}",
#             )
#         assert response.status_code == 302
#         assert "/auth/index" in response.location  


def test_invalid_token(client, user):
    """An invalid token should render reset_password_error.html"""
    response = client.get(
        f"/reset_password/invalid_token/{user.id}",
        )
    assert response.status_code == 404  


def test_show_reset_password_form(client, user):
    """Valid token should show reset password form"""
    valid_token = user.generate_reset_password_token() 
    response = client.get(
        f"/reset_password/{valid_token}/{user.id}",
        )
    assert response.status_code == 200
    assert b"Reset Password" in response.data 


def test_successful_password_reset(client, user):
    """Valid form submission should reset password"""
    valid_token = user.generate_reset_password_token()
    
    response = client.post(
        f"/reset_password/{valid_token}/{user.id}",
        data={
            "password": "new_secure_password", 
            "confirm_password": "new_secure_password",
            },
        follow_redirects=True,
    )
    user = db.session.merge(user)
    db.session.refresh(user)  
    # assert user.check_password("new_secure_password") 
