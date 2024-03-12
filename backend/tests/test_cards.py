import pytest
from app import app, db
from app.models import User, Study, QSet
from datetime import datetime, timedelta
import json
from flask import url_for
from tests import client


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
        qset1 = QSet(title='QSet 1',
                     description='This is a set of cards',
                     creator=user1)

        db.session.add(user1)
        db.session.add(study1)
        db.session.commit()


def test_create_card(client):
    user_id = User.query.first().id
    qset_id = QSet.query.first().id
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is a card', 'creator_id': user_id, 'qset_id': qset_id})
    id = response.json['id']
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'text': 'This is a card'}.items()
