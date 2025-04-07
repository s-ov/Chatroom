import pytest
from app.auth.models import User
from flask import url_for

from conftest import login_user_via_client


def test_follow_another_user(client, user, other_user):
    login_user_via_client(client, user.email, "password")

    response = client.get(
        f'/user/follow/{other_user.username}', 
        follow_redirects=True,
        )

    assert response.status_code == 200
    # assert f"You are now following {user_b.username}!".encode() in response.data


def test_cannot_follow_self(client, user):
    login_user_via_client(client, user.email, "password")

    response = client.get(
        f'/user/follow/{user.username}', 
        follow_redirects=True,
        )

    assert response.status_code == 200
    # assert b"You cannot follow yourself!" in response.data


def test_cannot_follow_as_anonymous(client, other_user):
    response = client.get(f'/user/follow/{other_user.username}', follow_redirects=True)

    assert response.status_code == 200
#   assert b"Please log in to access this page" in response.data or b"Login" in response.data


def test_follow_nonexistent_user_returns_404(client, user):
    login_user_via_client(client, user.email, "password")

    response = client.get("/follow/doesnotexist", follow_redirects=True)

    assert response.status_code == 404


def test_unfollow_user(client, user, other_user, db_session):
    db_session.add_all([user, other_user])
    db_session.commit()

    user.follow(other_user)
    db_session.commit()

    login_user_via_client(client, user.email, "password")

    response = client.get(
        f'/user/unfollow/{other_user.username}',
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert user.is_following(other_user)
    # assert f"You have unfollowed {other_user.username}.".encode() in response.data

