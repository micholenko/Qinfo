from app import db, app
from app.models import User, Study, StudyRound, QSet, Response, Card, CardPosition
from datetime import datetime
import json


def fill_db():
    # Create some users
    with app.app_context():
        db.drop_all()
        db.create_all()
        user1 = User(name='user1', email='test1@example.com',
                     role='participant')
        user2 = User(name='user2', email='test2@example.com',
                     role='participant')

        # Create studies
        study1 = Study(title='Study 1', description='This is a study', created_time=datetime.now(),
                       status='not_started', question='What is your favorite color?',
                       distribution=json.dumps([1, 2, 3, 2, 1]))
        study2 = Study(title='Study 2', description='This is another study', created_time=datetime.now(),
                       status='not_started', question='What is your favorite animal?',
                       distribution=json.dumps([1,1,2, 3, 3, 3, 2,1,1]))

        qset1 = QSet(title='QSet 1', description='This is a set of cards',
                     creator=user1, studies=[study1, study2])

        round1 = StudyRound(study=study1)
        round2 = StudyRound(study=study1)

        round3 = StudyRound(study=study2)

        # add 4 responses to round1
        response1 = Response(respondent=user1, round=round1,
                             time_submitted=datetime.now())
        response2 = Response(respondent=user2, round=round1,
                             time_submitted=datetime.now())
        
        response3 = Response(respondent=user1, round=round3,
                             time_submitted=datetime.now())

        # add 10 cards
        for i in range(10):
            card = Card(text=f'This is card {i}', creator=user1, qSet=qset1)
            db.session.add(card)

        # add all cards to responses

        for i in range(10):
            card = db.session.get(Card, i+1)
            position1 = CardPosition(
                card=card, response=response1, column=i, row=0)
            position2 = CardPosition(
                card=card, response=response2, column=10-i, row=0)
            db.session.add(position1)
            db.session.add(position2)

        # db session add all users and studies

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(study1)
        db.session.add(study2)
        db.session.add(round1)
        db.session.add(round2)
        db.session.add(qset1)
        db.session.add(response1)
        db.session.add(response2)
        db.session.add(response3)
        db.session.commit()


if __name__ == "__main__":
    fill_db()
