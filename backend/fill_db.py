from app import db, app
from app.models import User, Study, Round, QSet, Response, Card, CardPosition, UserStudyAssociation
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
        
        qset1 = QSet(title='QSet 1', description='This is a set of cards',
                     creator=user1, studies=[study1])


        round1 = Round(study=study1, created_time=datetime.now(), name='Round 1')
        round2 = Round(study=study1, created_time=datetime.now(), name='Round 2')
        round4 = Round(study=study1, created_time=datetime.now(), name='Round 3')


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
            # position_offset += random.randint(0, 9)

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
            # position_offset += random.randint(0, 9)

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
            # position_offset += random.randint(0, 9)

        # db session add all users and studies

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(study1)
        db.session.add(round1)
        db.session.add(round2)
        db.session.add(round4)
        db.session.add(qset1)
        db.session.commit()

        # get all cards in qset1 join with Cards table


        # create a study of 5 rounds with 40 users, with distribution: [1,2,3,4,5,6,7,6,5,4,3,2,1] total cards being 47
        # each user has a response in each round

        study3 = Study(title='Study 3', description='This is a study', created_time=datetime.now(),
                          status='not_started', question='What is your favorite color?',
                          distribution=json.dumps([1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]),
                          col_values=json.dumps([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]))
        
        qset2 = QSet(title='QSet 2', description='This is a set of cards',
                        creator=user1, studies=[study3])
        

        # create all possible positions from distribution

        positions = []
        for index, height in enumerate(json.loads(study3.distribution)):
            for j in range(height):
                positions.append((index, j))


        round5 = Round(study=study3, created_time=datetime.now(), name='Round 1')
        round6 = Round(study=study3, created_time=datetime.now(), name='Round 2')
        round7 = Round(study=study3, created_time=datetime.now(), name='Round 3')
        round8 = Round(study=study3, created_time=datetime.now(), name='Round 4')
        round9 = Round(study=study3, created_time=datetime.now(), name='Round 5')

        db.session.add(study3)
        db.session.add(qset2)
        db.session.add(round5)
        db.session.add(round6)
        db.session.add(round7)
        db.session.add(round8)
        db.session.add(round9)
        db.session.commit()

        cards = []
        
        for i in range(49):
            card = Card(text='Lorem ipsum dolor sit amet, consectetur adipiscing elit'+str(i), creator=user1, qset=qset2)
            cards.append(card)
            db.session.add(card)

        users = []
        for i in range(40):
            user = User(name='study3user'+str(i), email='study3user'+str(i)+'@example.com',
                        role='participant', password='password')
            db.session.add(user)
            db.session.commit()
            association = UserStudyAssociation(
                user_id=user.id, study_id=study3.id, role='participant')
            db.session.add(association)
            users.append(user)

        for round in study3.rounds:
            for i, user in enumerate(users):
                response = Response(respondent=user, round=round,
                                    time_submitted=datetime.now())
                
                db.session.add(response)
                positions_tmp = positions.copy()

                for j in range(len(cards)):
                    rand = random.randint(0, len(positions_tmp)-1)
                    position = CardPosition(
                        card=cards[j], response=response, column=positions_tmp[rand][0], row=positions_tmp[rand][1])
                    db.session.add(position)
                    positions_tmp.pop(rand)

        db.session.commit()




if __name__ == "__main__":
    fill_db()
