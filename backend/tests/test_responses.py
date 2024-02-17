from tests import client
import pytest
from app.models import User, Study, StudyRound, db, Card, QSet
from datetime import datetime
from flask import url_for
from app import app
from datetime import datetime, timedelta

# for each test create objects in the database

def setup_db():
    # create a new user
    user1 = User(name='John Doe',
                 email='reeeee',
                 role='researcher')
    # create a new study

    qset1 = QSet(title='QSet 1',
                    description='This is a set of cards',
                    creator=user1)
    

    study1 = Study(title='Study 1',
                   question='What is your favorite color?',
                   description='This is a study about colors',
                   created_time=datetime.now(),
                   submit_time=datetime.now() + timedelta(days=7),
                   status='not_started',
                   q_set=qset1,
                   )
    round1 = StudyRound(study=study1)

    for i in range(10):
        card = Card(text=f'This is card {i}',
                    creator=user1,
                    qSet=study1.q_set)
        db.session.add(card)
    db.session.add(user1)
    db.session.add(study1)
    db.session.add(round1)
    db.session.commit()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Qinfo'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    with app.app_context():
        with app.test_client() as client:
            db.create_all()
            setup_db()
            yield client
            db.session.remove()
            db.drop_all()


def test_add_response(client):
    response = client.post(url_for('add_response'), json={
                           'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
    assert response.status_code == 200
    assert response.json.items() >= {
        'respondent_id': 1, 'round_id': 1}.items()
    

def test_get_responses(client):
    response = client.get(url_for('get_responses'))
    assert response.status_code == 200
    assert response.json == []

    response = client.post(url_for('add_response'), json={
                           'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
    assert response.status_code == 200

    response = client.get(url_for('get_responses'))
    assert response.status_code == 200
    assert response.json[0].items() >= {
        'respondent_id': 1, 'round_id': 1}.items()
    

def test_add_cards(client):
    response = client.post(url_for('add_response'), json={
                            'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
    cards = []
    cards_db = Card.query.all()
    for card_db, i in zip(cards_db, range(len(cards_db))):
        cards.append({'id': card_db.id, 'column': i, 'row': 0})
    ret = client.post(url_for('add_cards', id=1), json={'cards': cards})
    assert ret.status_code == 200

def test_get_cards(client):
    response = client.post(url_for('add_response'), json={
                            'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
    cards = []
    cards_db = Card.query.all()
    for card_db, i in zip(cards_db, range(len(cards_db))):
        cards.append({'id': card_db.id, 'column': i, 'row': 0})
    ret = client.post(url_for('add_cards', id=1), json={'cards': cards})
    assert ret.status_code == 200

    ret = client.get(url_for('get_cards', id=1))
    print(ret.json)
    assert ret.status_code == 200
    assert ret.json == cards