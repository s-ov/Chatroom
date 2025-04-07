import pytest
from app.posts.models import Post
from app.auth.models import User
from app.extensions import db

from flask import url_for
from flask_login import login_user


def login_user_via_client(client, email, password):
    return client.post(
        '/auth/login', 
        data={
            'email': email,
            'password': password,
        }, 
        follow_redirects=True,
        )


def test_author_can_delete_own_post(client, user, post_by_author):
    login_user_via_client(client, user.email, 'password')

    response = client.post(
        f'/post/delete_post/{post_by_author.id}', 
        follow_redirects=True,
        )

    assert response.status_code == 200
    assert db.session.get(Post, post_by_author.id) is not None


def test_user_cannot_delete_others_post(client, other_user, post_by_author):
    login_user_via_client(client, other_user.email, 'password')

    response = client.post(
        f'/post/delete_post/{post_by_author.id}', 
        follow_redirects=True,
        )

    assert response.status_code == 200
    assert Post.query.get(post_by_author.id) is not None


def test_anonymous_user_cannot_delete_post(client, post_by_author):
    response = client.post(
        f'/post/delete_post/{post_by_author.id}', 
        follow_redirects=True,
        )

    assert b'Please log in to access this page' in response.data or b'Login' in response.data
    assert Post.query.get(post_by_author.id) is not None
