import pytest
from flask import url_for
from app import app, db
from app.models import Study
from datetime import datetime

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

def test_hello_world(client):
    response = client.get(url_for('hello_world'))
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_create_study(client):
    response = client.post(url_for('create_study'), json={'title': 'Test Study', 'question': 'What is your favorite color?',
                                                         'description': 'This is a study about colors'})
    assert response.status_code == 200
    assert response.json.items() >= {'id': 1, 'title': 'Test Study', 'question': 'What is your favorite color?',
                              'description': 'This is a study about colors', 'status': 'not_started'}.items()

def test_get_study(client):
    # create a study
    study = Study(title='Test Study', question='What is your favorite color?',
                  description='This is a study about colors', created_time= datetime.now(),
                  status='not_started')
    db.session.add(study)
    db.session.commit()
    response = client.get(url_for('get_study', id=1))
    assert response.status_code == 200
    assert response.json.items() >= {'id': 1, 'title': 'Test Study', 'question': 'What is your favorite color?',
                              'description': 'This is a study about colors', 'status': 'not_started'}.items()
    
def test_get_studies(client):
    response = client.get(url_for('get_studies'))
    assert response.status_code == 200
    assert response.json == []

    study = Study(title='Test Study', question='What is your favorite color?',
                  description='This is a study about colors', created_time= datetime.now(),
                  status='not_started')
    db.session.add(study)
    db.session.commit()

    response = client.get(url_for('get_studies'))
    assert response.status_code == 200
    assert response.json[0].items() >= {'id': 1, 'title': 'Test Study', 'question': 'What is your favorite color?',
                              'description': 'This is a study about colors', 'status': 'not_started'}.items()
    

