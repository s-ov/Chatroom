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
)


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

