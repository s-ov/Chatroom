import pytest
from flask import url_for
from flask_login import login_user

from app.extensions import db
from app.auth.models import User


@pytest.fixture
def test_user(app):
    """Create a test user in the database."""
    with app.app_context():
        user = User(
            username="testuser", 
            email="testuser@example.com",
            )
        user.set_password("securepassword")  
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()
        

def test_logout(client, app, test_user):
    """Test user logout functionality."""
    with app.test_request_context():
        login_url = url_for('auth.login')
        logout_url = url_for('auth.logout')
    # Log in user
    client.post(
        login_url,
        data={
            "username": "testuser", 
            "password": "securepassword",
            },
        follow_redirects=True
    )

    # Log out the user
    response = client.get(logout_url, follow_redirects=True)

    assert response.status_code == 200  
    assert b'Login' in response.data or 'Авторизація'.encode('utf-8') in response.data  
