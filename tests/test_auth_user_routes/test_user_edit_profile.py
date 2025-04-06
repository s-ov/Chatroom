import pytest
from flask import url_for
from app import db
from app.auth.models import User  
from app.auth.user_forms import EditProfileForm  

# def test_edit_profile_success(logged_in_client, user, app):
#     """Test successfully updating a profile."""
#     new_username = "updated_user"
#     new_bio = "This is an updated bio."

#     response = logged_in_client.post(
#         url_for("user.edit_profile"),
#         data={"username": new_username, "bio": new_bio},
#         follow_redirects=True
#     )

#     assert response.status_code == 200

#     with app.app_context():
#         db.session.refresh(user)
#         assert user.username == new_username
#         assert user.bio == new_bio
def test_edit_profile_success(logged_in_client, user, app):
    """Test successfully updating a profile."""

    logged_in_client.post(url_for("auth.login"), data={
        "username": user.username,
        "password": "password123"
    }, follow_redirects=True)

    new_username = "updated_user"
    new_bio = "This is an updated bio."

    response = logged_in_client.post(
        url_for("user.edit_profile"),
        data={"username": new_username, "bio": new_bio},
        follow_redirects=True
    )

    print(response.data.decode())  # Debugging: See if the edit was successful

    assert response.status_code == 200

    with app.app_context():
        updated_user = db.session.get(User, user.id)  # Re-fetch user from DB
        assert updated_user.username == new_username  # Should pass if update was successful
        assert updated_user.bio == new_bio



# def test_edit_profile_invalid_data(logged_in_client, user, app):
#     """Test profile update with invalid username (too short)."""
#     invalid_username = "a" 

#     response = logged_in_client.post(
#         url_for("user.edit_profile"),
#         data={"username": invalid_username, "bio": "Valid bio"},
#         follow_redirects=True
#     )

#     assert response.status_code == 200
#     assert b"This field must be at least 3 characters long." in response.data  # Adjust based on form validation messages
#     with app.app_context():
#         db.session.refresh(user)
#         assert user.username != invalid_username  # Ensure username didn't change


# def test_edit_profile_get_request(logged_in_client, user):
#     """Test loading the edit profile page with a GET request."""
#     response = logged_in_client.get(url_for("user.edit_profile"))
    
#     assert response.status_code == 200
#     assert b'Edit profile' in response.data  # Ensure template loads
#     assert f'value="{user.username}"'.encode() in response.data  # Pre-filled form check


# def test_edit_profile_unauthenticated(client):
#     """Test that an unauthenticated user cannot access the profile edit page."""
#     response = client.get(url_for("user.edit_profile"), follow_redirects=True)
    
#     assert response.status_code == 200
#     assert b"Please log in to access this page." in response.data  # Adjust based on your login message
