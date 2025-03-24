import pytest
from flask import url_for
from app import create_app, db
from app.auth.models import User
from app.auth.forms import RegistrationForm


def test_username_unique_validation(client):
    """Test that the form raises a validation error if the username already exists."""
    
    existing_user = User(
        username='testuser', 
        email='test@example.com',
        )
    existing_user.set_password('securepassword')
    db.session.add(existing_user)
    db.session.commit()

    form_data = {
        'username': 'testuser',
        'email': 'new@example.com',
        'password': 'newpassword',
        'password2': 'newpassword'
    }
    form = RegistrationForm(data=form_data)
    # form.validate_username(form.username)    raises ValidationError
    form.validate()
    assert 'Користувач з таким іменем вже зареєстрований.' in form.username.errors


def test_email_unique_validation(client):
    """Test that the form raises a validation error if the email already exists."""
    
    existing_user = User(username='newuser', email='test@example.com')
    existing_user.set_password('securepassword')
    db.session.add(existing_user)
    db.session.commit()

    form_data = {
        'username': 'anotheruser',
        'email': 'test@example.com',
        'password': 'newpassword',
        'password2': 'newpassword'
    }
    form = RegistrationForm(data=form_data)
    form.validate()
    
    assert 'No such email. First, register.' in form.email.errors


def test_password_match_validation(client):
    """Test that the form raises a validation error if passwords don't match."""
    
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'password2': 'password456'  
    }
    form = RegistrationForm(data=form_data)
    is_valid = form.validate()

    assert not is_valid, "Form should not be valid when passwords do not match."
    assert 'Field must be equal to password.' in form.password2.errors


def test_valid_registration(client, app):
    """Test successful registration."""
    with app.test_request_context():  
        register_url = url_for('auth.register')
    form_data = {
        'username': 'validuser',
        'email': 'valid@example.com',
        'password': 'password123',
        'password2': 'password123'
    }
    response = client.post(
        register_url, 
        data=form_data, 
        follow_redirects=True,
        )
    assert response.status_code == 200

    user = User.query.filter_by(username='validuser').first()
    assert user is not None, "User should have been created in the database."
    
    assert user.check_password('password123'),\
          "Password should be correctly hashed and verified."
