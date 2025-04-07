from app.posts.models import Post
from conftest import login_user_via_client


def test_profile_page_post_submission(client, user, db_session):
    login_user_via_client(client, user.email, "password")

    response = client.post(
        f"/workflow/profile_page/{user.username}",
        data={"post": "This is a test post!"}, 
        follow_redirects=True
    )

    assert response.status_code == 200

    saved_post = Post.query.filter_by(
        user_id=user.id,
        body="This is a test post!"
    ).first()

    assert saved_post is None


def test_chatroom_post_submission(client, user, db_session):
    login_user_via_client(client, user.email, "password")

    response = client.post(
        f"/workflow/chatroom/{user.username}",
        data={"post": "Hello from the chatroom!"},
        follow_redirects=True,
    )

    assert response.status_code == 200

    saved_post = Post.query.filter_by(
        user_id=user.id,
        body="Hello from the chatroom!"
    ).first()

    assert saved_post is None

