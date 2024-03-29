# from tests import client
# import pytest
# from app.models import User, Study, Round, db, Card, QSet
# from datetime import datetime
# from flask import url_for
# from app import app
# from datetime import datetime, timedelta

# # for each test create objects in the database

# @pytest.fixture
# def setup_db():
#     print('setup_db responses')
#     # create a new user
#     user1 = User(name='John Doe',
#                  email='reeeee',
#                  role='researcher')
#     # create a new study

#     qset1 = QSet(title='QSet 1',
#                     description='This is a set of cards',
#                     creator=user1)
    

#     study1 = Study(title='Study 1',
#                    question='What is your favorite color?',
#                    description='This is a study about colors',
#                    created_time=datetime.now(),
#                    submit_time=datetime.now() + timedelta(days=7),
#                    status='not_started',
#                    qset=qset1,
#                    )
#     round1 = Round(study=study1)

#     for i in range(10):
#         card = Card(text=f'This is card {i}',
#                     creator=user1,
#                     qset=study1.qset)
#         db.session.add(card)
#     db.session.add(user1)
#     db.session.add(study1)
#     db.session.add(round1)
#     db.session.commit()

# def test_add_response(client):
#     response = client.post(url_for('add_response'), json={
#                            'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
#     assert response.status_code == 200
#     assert response.json.items() >= {
#         'respondent_id': 1, 'round_id': 1}.items()
    

# def test_get_responses(client):
#     response = client.get(url_for('get_responses'))
#     assert response.status_code == 200
#     assert response.json == []

#     response = client.post(url_for('add_response'), json={
#                            'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
#     assert response.status_code == 200

#     response = client.get(url_for('get_responses'))
#     assert response.status_code == 200
#     assert response.json[0].items() >= {
#         'respondent_id': 1, 'round_id': 1}.items()
    

# def test_add_cards(client):
#     response = client.post(url_for('add_response'), json={
#                             'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
#     cards = []
#     cards_db = Card.query.all()
#     for card_db, i in zip(cards_db, range(len(cards_db))):
#         cards.append({'id': card_db.id, 'column': i, 'row': 0})
#     ret = client.post(url_for('add_cards', id=1), json={'cards': cards})
#     assert ret.status_code == 200

# def test_get_cards(client):
#     response = client.post(url_for('add_response'), json={
#                             'respondent_id': 1, 'round_id': 1, 'time_submitted': datetime.now()})
#     cards = []
#     cards_db = Card.query.all()
#     for card_db, i in zip(cards_db, range(len(cards_db))):
#         cards.append({'id': card_db.id, 'column': i, 'row': 0})
#     ret = client.post(url_for('add_cards', id=1), json={'cards': cards})
#     assert ret.status_code == 200

#     ret = client.get(url_for('get_cards', id=1))
#     print(ret.json)
#     assert ret.status_code == 200
#     assert ret.json == cards