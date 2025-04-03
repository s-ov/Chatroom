import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from config import config, TestingConfig, DevelopmentConfig
from app.extensions import (
    db, migrate, login, moment, babel, mail,
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
    mail.init_app(app)
    configure_logging(app)

    from app.auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth",)

    from app.auth.routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/user",)

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


def configure_logging(app):
    """Configure logging for Flask app"""

    log_level = logging.DEBUG if app.config["DEBUG"] else logging.INFO
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  
    log_file = os.path.join(log_dir, "app.log")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10240, backupCount=10
    )
    file_handler.setLevel(log_level)
    
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    app.logger.addHandler(console_handler)

    app.logger.info("Logging is configured.")
