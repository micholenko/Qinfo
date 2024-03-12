from app import db, app
from app.models import User, Study, StudyRound, QSet, Response, Card, CardPosition, UserStudyAssociation
from datetime import datetime
import json
import random


def fill_db():
    # Create some users
    with app.app_context():
        db.drop_all()
        db.create_all()
        user1 = User(name='john', email='john@example.com',
                     role='participant', password='password')
        user2 = User(name='james', email='james@example.com',
                     role='participant', password='password')

        # Create studies
        study1 = Study(title='Study 1', description='This is a study', created_time=datetime.now(),
                       status='not_started', question='What is your favorite color?',
                       distribution=json.dumps([1, 2, 3, 2, 1]),
                       col_values=json.dumps([-2, -1, 0, 1, 2]))
        study2 = Study(title='Study 2', description='This is another study', created_time=datetime.now(),
                       status='not_started', question='What is your favorite animal?',
                       distribution=json.dumps([1, 1, 2, 3, 3, 3, 2, 1, 1]),
                       col_values=json.dumps([-4, -3, -2, -1, 0, 1, 2, 3, 4]))

        qset1 = QSet(title='QSet 1', description='This is a set of cards',
                     creator=user1, studies=[study1, study2])

        round1 = StudyRound(study=study1)
        round2 = StudyRound(study=study1)
        round4 = StudyRound(study=study1)

        round3 = StudyRound(study=study2)

        response3 = Response(respondent=user1, round=round3,
                             time_submitted=datetime.now())

        # add 10 cards
        colors = ['red', 'blue', 'green', 'yellow',
                  'orange', 'purple', 'black', 'white', 'pink']
        for i in range(9):
            card = Card(text=colors[i], creator=user1, qset=qset1)
            db.session.add(card)

        # add all cards to responses

        positions = [
            [0, 0],
            [1, 0],
            [1, 1],
            [2, 0],
            [2, 1],
            [2, 2],
            [3, 0],
            [3, 1],
            [4, 0],
        ]

        users = []
        for i in range(10):
            user = User(name='user'+str(i), email='test'+str(i)+'@example.com',
                        role='participant', password='password')
            db.session.add(user)
            db.session.commit()
            association = UserStudyAssociation(
                user_id=user.id, study_id=study1.id, role='participant')
            db.session.add(association)
            users.append(user)
        position_offset = 0

        for i, user in enumerate(users):
            response = Response(respondent=user, round=round1,
                                time_submitted=datetime.now())

            db.session.add(response)
            for j in range(9):
                card = db.session.get(Card, j+1)
                index = (j + position_offset) % 9
                position = CardPosition(
                    card=card, response=response, column=positions[index][0], row=positions[index][1])
                db.session.add(position)
            position_offset += random.randint(0, 1)

        for i, user in enumerate(users):
            response = Response(respondent=user, round=round2,
                                time_submitted=datetime.now())

            db.session.add(response)
            for j in range(9):
                card = db.session.get(Card, j+1)
                index = (j + position_offset) % 9
                position = CardPosition(
                    card=card, response=response, column=positions[index][0], row=positions[index][1])
                db.session.add(position)
            position_offset += random.randint(0, 1)

        for i, user in enumerate(users):
            response = Response(respondent=user, round=round4,
                                time_submitted=datetime.now())

            db.session.add(response)
            for j in range(9):
                card = db.session.get(Card, j+1)
                index = (j + position_offset) % 9
                position = CardPosition(
                    card=card, response=response, column=positions[index][0], row=positions[index][1])
                db.session.add(position)
            position_offset += random.randint(0, 1)

        # db session add all users and studies

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(study1)
        db.session.add(study2)
        db.session.add(round1)
        db.session.add(round2)
        db.session.add(round3)
        db.session.add(round4)
        db.session.add(qset1)
        db.session.add(response3)
        db.session.commit()

        # get all cards in qset1 join with Cards table


if __name__ == "__main__":
    fill_db()
