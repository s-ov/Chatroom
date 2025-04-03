import sys
import os
import pytest

from flask import url_for

from app.auth.models import User

sys.path.insert(
    0, 
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../")),
    )

from app import create_app
from app.extensions import db

pytest_plugins = ["pytest_mock"]


@pytest.fixture
def app():
    app = create_app("testing")  
    app.config["SERVER_NAME"] = "localhost:5000"
    with app.app_context():
        db.create_all()  
        yield app
        db.session.remove()
        db.drop_all()  


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_client(client, user):
    """Logs in the test user before each request using the login route."""
    with client:
        response = client.post(
            url_for("auth.login"),
            data={"email": user.email, "password": user.set_password("testpassword")},
            follow_redirects=True
        )
        yield client  # Return the logged-in client


    
@pytest.fixture
def user(app):
    """Create a test user in the database."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")  
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email="test@example.com").first()
        return user


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    db.create_all()
    yield db.session
    db.session.rollback()
    db.drop_all()
