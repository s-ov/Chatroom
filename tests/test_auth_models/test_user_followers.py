import pytest
from app import db
from app.auth.models import User

@pytest.fixture
def setup_users(app):
    """Fixture to set up test users in the database."""
    with app.app_context():
        db.create_all()
        user1 = User(username="Alice", email="alice@example.com")
        user2 = User(username="Bob", email="bob@example.com")
        db.session.add_all([user1, user2])
        db.session.commit()
        yield user1, user2  # Return test users
        db.session.remove()
        db.drop_all()

def test_follow(app, setup_users):
    """Test if a user can follow another user."""
    user1, user2 = setup_users

    with app.app_context():
        user1.follow(user2)
        db.session.commit()

        assert user1.is_following(user2) is True
        assert user2.is_following(user1) is False

def test_unfollow(app, setup_users):
    """Test if a user can unfollow another user."""
    user1, user2 = setup_users

    with app.app_context():
        user1.follow(user2)
        db.session.commit()
        assert user1.is_following(user2) is True

        user1.unfollow(user2)
        db.session.commit()
        assert user1.is_following(user2) is False

def test_is_following(app, setup_users):
    """Test the is_following method."""
    user1, user2 = setup_users

    with app.app_context():
        assert user1.is_following(user2) is False
        user1.follow(user2)
        db.session.commit()
        assert user1.is_following(user2) is True
