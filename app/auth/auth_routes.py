from flask import (
    render_template, redirect, url_for, flash,
    )
from flask_login import (
    current_user, login_user, logout_user,
    )
from flask_babel import lazy_gettext as _
from app.extensions import db
from app.auth import auth_bp
from app.auth.models import User
from app.auth.forms import (
    RegistrationForm,
    LoginForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from app.auth.services import send_reset_password_email
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@auth_bp.route("/")
def index():
    "Render index page"
    return render_template("base.html", title="Main auth")


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    "Register a new user"

    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('auth.login'))
    
    return render_template(
        'auth/register.html', 
        title='Реєстрація', 
        form=form,
        )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    "Login current user"

    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Wrong username or password')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('auth.index'))

    return render_template(
        'auth/login.html', 
        title='Авторизація', 
        form=form,
        )


@auth_bp.route('/logout')
def logout():
    "Logout authorized user"
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    "Send reset password request"
    
    logger.debug("Reset password request initiated.")

    if current_user.is_authenticated:
        logger.debug(
            f"User {current_user.email} is already authenticated, redirecting to index.",
            )
        return redirect(url_for("auth.index"))
    
    form = ResetPasswordRequestForm()
    
    if form.validate_on_submit():
        logger.debug(f"Form submitted with email: {form.email.data}")

        user = User.query.filter_by(email=form.email.data).first()

        if user:
            logger.info(
                f"User found: {user.email}. Sending reset password email.",
                )
            send_reset_password_email(user)
            flash(
                "Instructions to reset your password were sent "
                "to your email address, if it exists in our system."
            )
        else:
            logger.warning(
                f"No user found with email: {form.email.data}",
                )
        return redirect(url_for("auth.reset_password_request"))

    logger.debug("Rendering reset password request page.")
    return render_template(
        "auth/reset_password_request.html", 
        title="Reset Password", 
        form=form,
    )


@auth_bp.route(
        "/reset_password/<token>/<int:user_id>", 
        methods=["GET", "POST"],
        )
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))

    user = User.validate_reset_password_token(token, user_id)
    if not user:
        return render_template(
            "auth/reset_password_error.html", 
            title="Reset Password error",
        )

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()

        return render_template(
            "auth/reset_password_success.html", 
            title="Reset Password success",
        )

    return render_template(
        "auth/reset_password.html", 
        title="Reset Password", 
        form=form,
    )
