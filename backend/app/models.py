
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Text, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from typing import List, Optional
from sqlalchemy import UniqueConstraint
from sqlalchemy import CheckConstraint
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
import json
from flask_login import UserMixin
from app import login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    # define str length
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    
    role: Mapped[str] = mapped_column(String(250), nullable=False)

    # revise if back_populates is necessary
    qsets: Mapped[List['QSet']] = relationship(back_populates='creator')
    cards: Mapped[List['Card']] = relationship(back_populates='creator')

    studies: Mapped[List['Study']] = relationship(back_populates='users', secondary='user_study_association')
    studies_association: Mapped[List['UserStudyAssociation']] = relationship(back_populates='user', viewonly=True)

    responses: Mapped[List['Response']] = relationship(back_populates='respondent')


    __table_args__ = (
        CheckConstraint(
            role.in_(['researcher', 'participant']),
            name='role_check'
        ),
    )

    def __repr__(self):
        return f"User('{self.name}')"


class Study(db.Model):
    __tablename__ = 'study'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    question: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    # store array of integers in mysql
    distribution: Mapped[List[int]] = mapped_column(String(120))
    col_values: Mapped[List[int]] = mapped_column(String(120))


    created_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    rounds: Mapped[List['Round']] = relationship(back_populates='study')

    qset_id: Mapped[Optional[int]] = mapped_column(ForeignKey('qset.id'))
    qset: Mapped[Optional['QSet']] = relationship(back_populates='studies')

    users: Mapped[List['User']] = relationship(back_populates='studies', secondary='user_study_association')
    users_association: Mapped[List['UserStudyAssociation']] = relationship(back_populates='study', viewonly=True)

    __table_args__ = (
        db.CheckConstraint(
            status.in_(['not_started', 'in_progress', 'completed']),
            name='status_check'
        ),
    )

    def __repr__(self):
        return f"Study('{self.title}')"

class UserStudyAssociation(db.Model):
    __tablename__ = 'user_study_association'    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    study_id: Mapped[int] = mapped_column(ForeignKey('study.id'), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='studies_association', viewonly=True)
    study: Mapped['Study'] = relationship(back_populates='users_association', viewonly=True)

    role: Mapped[str] = mapped_column(String(20), nullable=False)
    __table_args__ = (
        CheckConstraint(
            role.in_(['owner', 'participant', 'collaborator']),
        ),
    )   


class Round(db.Model):
    __tablename__ = 'study_round'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[Optional[str]] = mapped_column(Text)

    study_id: Mapped[int] = mapped_column(ForeignKey('study.id'))
    study: Mapped['Study'] = relationship(back_populates='rounds')

    created_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    start_time: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    end_time: Mapped[Optional[DateTime]] = mapped_column(DateTime)



    responses: Mapped[List['Response']] = relationship(back_populates='round')

    def __repr__(self):
        return f"Round('{self.study_id}')"

class QSet(db.Model):
    __tablename__ = 'qset'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    creator: Mapped['User'] = relationship(back_populates='qsets')

    cards: Mapped[List['Card']] = relationship(back_populates='qset')

    studies: Mapped[List['Study']] = relationship(back_populates='qset')

    def __repr__(self):
        return f"Qset('{self.title}')"


class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # arguably not necessary
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    creator: Mapped['User'] = relationship(back_populates='cards')

    qset_id: Mapped[int] = mapped_column(ForeignKey('qset.id'))
    qset: Mapped['QSet'] = relationship(back_populates='cards')

    # could make analysis easier 
    # positions: Mapped[List['CardPosition']] = relationship(back_populates='card')

    def __repr__(self):
        return f"Card('{self.text}')"


class Response(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    respondent_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    respondent: Mapped['User'] = relationship(back_populates='responses')

    round_id: Mapped[int] = mapped_column(ForeignKey('study_round.id'))
    round: Mapped['Round'] = relationship(back_populates='responses')

    time_submitted: Mapped[Optional[DateTime]] = mapped_column(DateTime)

    positions: Mapped[List['CardPosition']] = relationship(back_populates='response')

    __table_args__ = (UniqueConstraint('respondent_id', 'round_id', name='one_response_per_round'),)

    def __repr__(self):
        return f"Qtable to Study('{self.round_id} from {self.respondent}')"

class CardPosition(db.Model):
    __tablename__ = 'card_position'
    
    card_id: Mapped[int] = mapped_column(ForeignKey('card.id'), primary_key=True)
    # card: Mapped['Card'] = relationship(back_populates='positions')
    card: Mapped['Card'] = relationship()

    response_id: Mapped[int] = mapped_column(ForeignKey('response.id'), primary_key=True)
    response: Mapped['Response'] = relationship(back_populates='positions')

    column: Mapped[int] = mapped_column(Integer, nullable=False)
    row: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('response_id', 'column', 'row', name='one_card_per_position'),
    )

    def __repr__(self) -> str:
        return f'Card position on {self.response}: [{self.column}, {self.row}]'

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)