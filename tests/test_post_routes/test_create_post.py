import pytest
from flask import url_for
from app import db
from app.posts.models import Post
from app.auth.models import User 


def login_test_user(client, user):
    client.post(
        '/auth/login', 
        data={
        'email': user.email,
        'password': 'password'
        }, 
        follow_redirects=True,
        )
    

def test_get_create_post_view(client, user):
    login_test_user(client, user)

    response = client.get('/post/create_post')
    assert response.status_code == 200
    assert b'Create post' in response.data  


def test_post_create_post_view(client, logged_in_user, app):
    login_test_user(client, logged_in_user)

    assert Post.query.count() == 0

    response = client.post(
        '/post/create_post', 
        data={
        'post': 'Hello world!'
        }, 
        follow_redirects=True,
        )

    assert response.status_code == 200
    assert Post.query.count() == 1

    post = Post.query.first()
    assert post.body == 'Hello world!'
    assert post.user_id == logged_in_user.id
