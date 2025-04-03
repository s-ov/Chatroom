import pytest

import os
from io import BytesIO

from flask import url_for
from werkzeug.datastructures import FileStorage

from config import Config
from app.auth.models import User


def test_upload_profile_picture_success(logged_in_client, user, db_session):
    """Test successfully uploading a profile picture."""
    
    img_data = b'fake image data'  
    img_file = BytesIO(img_data)
    img_file.name = "ava2.jpg" 

    file_data = FileStorage(
        stream=img_file,
        filename="ava2.jpg",
        content_type="image/jpeg"
    )

    response = logged_in_client.post(
        url_for("user.upload_profile_picture", user_id=user.id),
        data={"profile_picture": file_data},
        content_type="multipart/form-data",
        follow_redirects=True
    )

    assert response.status_code == 200

    user = User.query.get(user.id)
    assert user.profile_picture == "ava2.jpg"

    uploaded_path = os.path.join(Config.UPLOAD_FOLDER, "ava2.jpg")
    if os.path.exists(uploaded_path):
        os.remove(uploaded_path)


# def test_upload_invalid_file_type(logged_in_client, user, app):
#     """Test uploading a file with an invalid extension."""
#     file_data = FileStorage(
#             stream=open("tests/conftest.py", "rb"),
#             filename="conftest.py",
#             content_type="application/x-msdownload"
#         )

#     response = logged_in_client.post(
#                 url_for("user.upload_profile_picture", user_id=user.id),
#                 data={"profile_picture": file_data},
#                 content_type="multipart/form-data",
#                 follow_redirects=True
#             )

#     assert response.status_code == 200       

    

def test_upload_without_login(client, user, app):
    """Test uploading a profile picture without being logged in."""
    with app.app_context():
        file_data = FileStorage(
            stream=open("tests/default.jpg", "rb"),
            filename="default.jpg",
            content_type="image/jpeg"
        )

        response = client.post(
            url_for("user.upload_profile_picture", user_id=user.id),
            data={"profile_picture": file_data},
            content_type="multipart/form-data",
            follow_redirects=True
        )

        assert response.status_code == 200  
        assert b"auth/login" in response.data  
        
