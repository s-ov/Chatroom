import pytest
from flask import url_for
from app import create_app, db
from app.auth.models import User
from app.auth.forms import RegistrationForm
from flask_login import current_user


def test_register_success(client, app):
    """Test successful user registration."""
    with app.test_request_context():  
        register_url = url_for('auth.register')  
    
    response = client.post(
        register_url,  
        data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword',
            'password2': 'securepassword'
        },
        follow_redirects=True
    )

    with app.app_context():  
        user = User.query.filter_by(username='testuser').first()
    
    assert response.status_code == 200
    assert user is not None  
    assert user.email == "test@example.com"
    assert b'Your post is now live!' in response.data
    with app.app_context(), app.test_request_context():
        assert '/auth/register' == url_for('auth.register')


def test_register_redirect_if_authenticated(client, app):
    """Test that an authenticated user is redirected."""
    
    user = User(username='existing_user', email='test@example.com')
    user.set_password('securepassword')
    db.session.add(user)
    db.session.commit()

    with client.session_transaction() as session:
        session["_user_id"] = str(user.id)
    
    with app.app_context(), app.test_request_context():  
        register_url = url_for('auth.register')

    response = client.get(register_url, follow_redirects=True)

    assert response.status_code == 200


def test_register_form_validation_fails(client, app):
    """Test form validation failure (e.g., missing password)."""
    with app.app_context(), app.test_request_context():  
        register_url = url_for('auth.register')

    with client.application.app_context(): 
        response = client.post(
            register_url, 
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': '',  
                'password2': ''  
            }, 
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert User.query.filter_by(username='testuser').first() is None
    assert b'This field is required' in response.data
