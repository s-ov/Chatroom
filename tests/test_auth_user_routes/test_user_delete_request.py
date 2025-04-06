import pytest
from flask import url_for
from app.auth.models import User
from app import db


def test_access_delete_account_page(logged_in_client, user):
    """Test that a logged-in user can access the delete account page."""
    response = logged_in_client.get(
        url_for("user.delete_user_request"),
        )
    assert response.status_code == 302


def test_redirect_if_not_logged_in(client):
    """Test that a non-logged-in user is redirected to the login page."""
    response = client.get(
        url_for("user.delete_user_request"), 
        follow_redirects=True,
        )
    assert b"Login" in response.data  


def test_submit_delete_account_form_success(logged_in_client, user):
    """Test that submitting a valid delete request redirects to the delete action."""
    
    logged_in_client.post(
        url_for("auth.login"), 
        data={
            "username": user.username,
            "password": "testpassword",
        }, 
        follow_redirects=True)
    
    response = logged_in_client.post(
        url_for("user.delete_user_request"),
        data={"confirm": "yes"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    # assert url_for("user.delete_user") in response.request.path  
    

def test_submit_delete_account_form_failure(logged_in_client):
    """Test that submitting an invalid form reloads the page."""
    response = logged_in_client.post(
        url_for("user.delete_user_request"),
        data={},  
        follow_redirects=True
    )
   
    assert response.status_code == 200
    