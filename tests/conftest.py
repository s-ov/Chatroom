import sys
import os
import pytest

sys.path.insert(
    0, 
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../")),
    )

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("testing")  
    with app.app_context():
        db.create_all()  
        yield app
        db.session.remove()
        db.drop_all()  


@pytest.fixture
def client(app):
    return app.test_client()
