import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    """Base configuration."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get("FLASK_DEBUG", False)
    TESTING = False
    LANGUAGES = ['en', 'es']

    POSTS_PER_PAGE = 5
    USERS_PER_PAGE = 1
    UPLOAD_FOLDER = os.path.join(
        os.getcwd(), 
        'app/static/uploads/profile_pics',
        )
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    RESET_PASS_TOKEN_MAX_AGE = 600

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME',)
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD',)
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URI', 
        'sqlite:///dev.db',
        )


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URI', 
        'sqlite:///test.db',
        )
    WTF_CSRF_ENABLED = False  


class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 
        'sqlite:///prod.db',
        )


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
