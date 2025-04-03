from flask import url_for, current_app


def handle_login_url(app):
    with app.test_request_context():  
        login_url = url_for('auth.reset_password_request')
    return login_url


def test_reset_password_page_access(client, app):
    """Test if reset password page loads correctly."""
    response = client.get(handle_login_url(app))
    assert response.status_code == 200
    assert b"Reset Password" in response.data


def test_reset_password_valid_email(client, user, mocker, app):
    """Test submitting a valid email and ensuring email is sent."""
    
    mock_send_email = mocker.patch(
        "app.auth.auth_routes.send_reset_password_email",
        )

    response = client.post(
        handle_login_url(app),  
        data={"email": user.email},  
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Instructions to reset your password" in response.data
    mock_send_email.assert_called_once_with(user)  


def test_reset_password_invalid_email(client, mocker, app):
    """Test submitting an invalid email."""
    mock_send_email = mocker.patch(
        "app.auth.auth_routes.send_reset_password_email",
        )

    response = client.post(
        handle_login_url(app),
        data={"email": "notexists@example.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    mock_send_email.assert_not_called()


def test_redirect_authenticated_user(client, user, app):
    """Test redirect if user is already authenticated."""
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)  # Simulate login

    response = client.get(
        handle_login_url(app), 
        follow_redirects=True,
        )

    assert response.status_code == 200
