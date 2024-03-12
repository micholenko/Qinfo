import pytest
from flask import url_for
from app import app, db
from app.models import User, Study
from datetime import datetime, timedelta
from tests import client
import json


@pytest.fixture
def setup_db():
    with app.app_context():
        db.create_all()
        # create a new user
        user1 = User(name='John Doe',
                     email='reeeee',
                     role='researcher',
                     password='password'
                     )
        # create a new study
        study1 = Study(title='Study 1',
                       question='What is your favorite color?',
                       description='This is a study about colors',
                       created_time=datetime.now(),
                       submit_time=datetime.now() + timedelta(days=7),
                       status='not_started',
                       distribution=json.dumps([1, 2, 3, 2, 1]),
                       col_values=json.dumps([-2, -1, 0, 1, 2])
                       )

        db.session.add(user1)
        db.session.add(study1)
        db.session.commit()


def test_create_qset(client):
    user_id = User.query.first().id
    response = client.post(url_for('qsets.create_qset'), json={
                           'title': 'Test QSet', 'description': 'This is a set of cards', 'creator_id': user_id})
    id = response.json['id']
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'title': 'Test QSet', 'description': 'This is a set of cards'}.items()

def test_get_qset(client):
    user_id = User.query.first().id
    response = client.post(url_for('qsets.create_qset'), json={
                           'title': 'Test QSet', 'description': 'This is a set of cards', 'creator_id': user_id})
    id = response.json['id']
    response = client.get(url_for('qsets.get_qset', id=id))
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'title': 'Test QSet', 'description': 'This is a set of cards'}.items()
    

def test_get_qsets(client):
    response = client.get(url_for('qsets.get_qsets'))
    assert response.status_code == 200
    assert response.json == []

    user_id = User.query.first().id
    response = client.post(url_for('qsets.create_qset'), json={
                           'title': 'Test QSet', 'description': 'This is a set of cards', 'creator_id': user_id})
    id = response.json['id']

    response = client.get(url_for('qsets.get_qsets'))
    assert response.status_code == 200
    assert response.json[0]['id'] == id
