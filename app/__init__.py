from flask import Flask, render_template
from config import config, TestingConfig, DevelopmentConfig
from app.extensions import (
    db, migrate, login, moment, babel,
    )


def create_app(config_name='development'):
    "Create a Flask app with the application factory"

    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config.from_object(config["testing"])
    else:
        app.config.from_object(config["development"])

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth",)

    @app.route("/")
    def main():
        "Render initial page"
        return render_template("base.html", title="Main")

    from app.auth.models import User

    @app.shell_context_processor
    def make_shell_context():
        """
        Create a shell context that adds the database instance
        and models to the shell session.
        You can work in < flask shell > without importing.
        """
        return {"db": db, "User": User}


    return app
