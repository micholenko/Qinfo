import pytest
from app import app, db

@pytest.fixture
def setup_db():
    print('setup_db default')
    pass

@pytest.fixture
def client(setup_db):
    print('client')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Qinfo'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    with app.app_context():
        with app.test_client() as client:
            yield client
            db.session.remove()
            db.drop_all()

    