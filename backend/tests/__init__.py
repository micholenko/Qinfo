import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Qinfo'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    with app.app_context():
        with app.test_client() as client:
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()