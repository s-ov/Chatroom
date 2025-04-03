from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash, check_password_hash,
)
from itsdangerous import (
    URLSafeTimedSerializer, 
    BadSignature, 
    SignatureExpired,
    )
from app.extensions import db, login

import logging

logger = logging.getLogger(__name__)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


followers = db.Table('followers',
                     db.metadata,
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
                     extend_existing=True,
            )


class User(UserMixin, db.Model):
    "Class represents User instance."
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    bio = db.Column(db.String(500))
    profile_picture = db.Column(db.String(255), nullable=True,)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<User: {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_password_token(self):
        "Generate a secure password reset token"
        logger.debug(
            f"Generating reset password token for user ID: {self.id},\
              Email: {self.email}",
              )
        
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = serializer.dumps(self.email, salt=self.password_hash)

        logger.debug(f"Generated token for user ID {self.id}: {token}")
        return token
    
    @staticmethod
    def validate_reset_password_token(token: str, user_id: int):
        "Validate the password reset token"
        logger.debug(
            f"Validating reset password token for user ID: {user_id}",
            )
        
        user = db.session.get(User, user_id)

        if user is None:
            logger.warning(
                f"User with ID {user_id} not found during password reset validation.",
                )
            return None

        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        try:
            token_user_email = serializer.loads(
                token,
                max_age=current_app.config.get(
                    "RESET_PASS_TOKEN_MAX_AGE", 
                    3600,
                    ),  
                salt=user.password_hash,
            )
            logger.debug(f"Token successfully decoded for user ID {user_id}")

        except SignatureExpired:
            logger.warning(f"Token expired for user ID {user_id}")
            return None

        except BadSignature:
            logger.warning(f"Invalid token signature for user ID {user_id}")
            return None

        if token_user_email != user.email:
            logger.warning(
                f"Token email {token_user_email} does not match user email\
                  {user.email} for user ID {user_id}",
                )
            return None

        logger.info(f"Reset password token validated successfully for user ID {user_id}")
        return user

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """Check if the current user follows another user."""
        if user is None:
            return False  
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
