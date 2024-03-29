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

# TODO: join the two tests into one
def test_create_card(client):
    user_id = User.query.first().id
    qset_id = QSet.query.first().id
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is a card', 'creator_id': user_id, 'qset_id': qset_id})
    id = response.json['id']
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'text': 'This is a card'}.items()
    
def test_get_card(client):
    user_id = User.query.first().id
    qset_id = QSet.query.first().id
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is a card', 'creator_id': user_id, 'qset_id': qset_id})
    id = response.json['id']
    response = client.get(url_for('cards.get_card', id=id))
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'text': 'This is a card'}.items()
    
def test_get_cards(client):
    response = client.get(url_for('cards.get_cards'))
    assert response.status_code == 200
    assert response.json == []
    user_id = User.query.first().id
    qset_id = QSet.query.first().id
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is a card', 'creator_id': user_id, 'qset_id': qset_id})
    assert response.status_code == 200
    response = client.get(url_for('cards.get_cards'))
    assert response.status_code == 200
    assert response.json[0].items() >= {
        'id': 1, 'text': 'This is a card'}.items()
    assert len(response.json) == 1
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is another card', 'creator_id': user_id, 'qset_id': qset_id})
    assert response.status_code == 200
    response = client.get(url_for('cards.get_cards'))
    assert response.status_code == 200
    assert response.json[1].items() >= {
        'id': 2, 'text': 'This is another card'}.items()
    assert len(response.json) == 2

def test_patch_card(client):
    user_id = User.query.first().id
    qset_id = QSet.query.first().id
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is a card', 'creator_id': user_id, 'qset_id': qset_id})
    id = response.json['id']
    response = client.patch(url_for('cards.update_card', id=id), json={
                            'text': 'This is a new card'})
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'text': 'This is a new card'}.items()
    response = client.get(url_for('cards.get_card', id=id))
    assert response.status_code == 200
    assert response.json.items() >= {
        'id': id, 'text': 'This is a new card'}.items()
    
def test_delete_card(client):
    user_id = User.query.first().id
    qset_id = QSet.query.first().id
    response = client.post(url_for('cards.create_card'), json={
                           'text': 'This is a card', 'creator_id': user_id, 'qset_id': qset_id})
    id = response.json['id']
    response = client.get(url_for('cards.get_cards'))
    assert response.status_code == 200
    assert len(response.json) == 1
    response = client.delete(url_for('cards.delete_card', id=id))
    assert response.status_code == 200
    response = client.get(url_for('cards.get_cards'))
    assert response.status_code == 200
    assert response.json == []
