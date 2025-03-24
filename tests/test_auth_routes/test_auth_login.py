import pytest
from flask import url_for
from flask_login import login_user

from app.extensions import db
from app.auth.models import User


def handle_login_url(app):
    with app.test_request_context():  
        login_url = url_for('auth.login')
    return login_url


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


def test_login_valid_user(client, test_user, app):
    """Test login with valid credentials."""
    
    response = client.post(
        handle_login_url(app),
        data={
            'username': 'testuser',
            'password': 'securepassword',
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Wrong username or password' not in response.data  
    assert b'Logout' in response.data or 'Вийти'.encode('utf-8') in response.data  


def test_login_invalid_username(client, test_user, app):
    """Test login with an invalid username."""
    response = client.post(
        handle_login_url(app),
        data={
            'username': 'wronguser', 
            'password': 'securepassword',
            },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Wrong username or password" in response.data  


def test_login_wrong_password(client, test_user, app):
    """Test login with incorrect password."""
    response = client.post(
        handle_login_url(app),
        data={
            'username': 'testuser', 
            'password': 'wrongpassword',
            },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Wrong username or password" in response.data


def test_redirect_if_already_logged_in(client, test_user, app):
    """Test that logged-in users are redirected to the index page."""
    with app.app_context(), app.test_request_context(): 
        login_user(test_user)  
        response = client.get(handle_login_url(app), follow_redirects=True)

        assert response.status_code == 200


def test_login_remember_me(client, test_user, app):
    """Test that the 'remember me' checkbox works."""
    response = client.post(
        handle_login_url(app),
        data={
            'username': 'testuser', 
            'password': 'securepassword', 
            'remember_me': 'on',
            },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Logout' in response.data
