# test rounds
import pytest
from app import app, db
from app.models import Study, Round, Response, Card
from tests import client
from flask import url_for
from datetime import datetime, timedelta
import json


@pytest.fixture
def setup_db():
    with app.app_context():
        db.create_all()
        # create a new study
        study1 = Study(title='Study 1',
                       question='What is your favorite color?',
                       description='This is a study about colors',
                       created_time=datetime.now(),
                       status='not_started',
                       distribution=json.dumps([1, 2, 3, 2, 1]),
                       col_values=json.dumps([-2, -1, 0, 1, 2])
                       )
        db.session.add(study1)
        db.session.commit()


def test_create_round(client):
    study_id = Study.query.first().id
    response = client.post(url_for('rounds.create_round'), json={
                           'study_id': study_id
                           })
    id = response.json['id']
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'study_id': study_id, 'name': 'Round 1'}.items()
    

def test_get_round(client):
    study_id = Study.query.first().id
    response = client.post(url_for('rounds.create_round'), json={
                           'study_id': study_id
                           })
    id = response.json['id']
    response = client.get(url_for('rounds.get_round', id=id))
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'study_id': study_id, 'name': 'Round 1'}.items()
    
