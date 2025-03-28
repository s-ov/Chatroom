from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from flask_mailman import Mail

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Авторизуйтесь, щоб увійти на дану сторінку.')

moment = Moment()
babel = Babel()
mail = Mail()
