from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from app.models import User, QSet, Study, UserStudyAssociation, StudyRound, Card, Response, CardPosition
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/Qinfo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import endpoints



# with app.app_context():
#     # remove all entries in the database
#     db.drop_all()
#     db.create_all()

#     # create a new user
#     user1 = User(name='John Doe',
#                  email='reeeee',
#                  role='researcher')
#     # create a new study
#     qset1 = QSet(title='QSet 1',
#                  description='This is a set of cards',
#                  creator=user1)

#     study1 = Study(title='Study 1',
#                    question='What is your favorite color?',
#                    description='This is a study about colors',
#                    created_time=datetime.now(),
#                    submit_time=datetime.now() + timedelta(days=7),
#                    status='not_started',
#                    q_set=qset1
#                    )
#     # add user as owner to the study
#     user_study_association = UserStudyAssociation(user=user1, study=study1, role='owner')


#     round1 = StudyRound(study=study1)
#     round2 = StudyRound(study=study1)

#     # # create a new qset

#     # create 10 cards
#     for i in range(10):
#         card = Card(text=f'This is card {i}',
#                     creator=user1,
#                     qSet=qset1)
#         db.session.add(card)

#     db.session.add(user1)
#     db.session.add(study1)
#     db.session.add(qset1)

#     response = Response(respondent=user1, round=round1, time_submitted=datetime.now())
    
#     CardPosition(card=Card.query.get(1), response=response, column=0, row=0)
#     CardPosition(card=Card.query.get(2), response=response, column=0, row=1)
#     CardPosition(card=Card.query.get(3), response=response, column=1, row=0)
#     CardPosition(card=Card.query.get(4), response=response, column=1, row=1)
#     CardPosition(card=Card.query.get(5), response=response, column=2, row=0)
#     CardPosition(card=Card.query.get(6), response=response, column=2, row=1)
#     CardPosition(card=Card.query.get(7), response=response, column=2, row=2)

#     db.session.add(response)

#     db.session.commit()

#     # order by column then by row
    
#     # cards = CardPosition.query.filter_by(response_id=response.id).order_by(CardPosition.column, CardPosition.row).all()
#     columns = 3 # hardcoded for now
