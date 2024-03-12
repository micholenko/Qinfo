from app.models import Card, Response, User, Study
from app import db
from app import login_manager
import pandas as pd


def get_card_matrix(id):
    cards = Card.query.filter_by(qset_id=1).all()
    responses = Response.query.filter_by(round_id=id).all()
    card_positions = []
    for response in responses:
        card_positions.extend(response.positions)

    data = []
    for card in cards:
        col = [card_position for card_position in card_positions if card_position.card == card]
        columns = tuple(card_position.column - 2 for card_position in col)
        data.append(columns)

    return data


def get_user_rounds(id):
    cards = Card.query.filter_by(qset_id=1).all()
    responses = Response.query.filter_by(respondent_id=id).all()
    card_positions = []
    for response in responses:
        card_positions.extend(response.positions)

    data = []
    for card in cards:
        col = [card_position for card_position in card_positions if card_position.card == card]
        columns = tuple(card_position.column - 2 for card_position in col)
        data.append(columns)
    print(data)
    return data

def get_cards_of_round(id):
    cards = Card.query.filter_by(qset_id=1).all()
    responses = Response.query.filter_by(round_id=id).all()
    card_positions = []
    for response in responses:
        card_positions.extend(response.positions)

    data = []
    for card in cards:
        col = [
            card_position for card_position in card_positions if card_position.card == card]
        columns = tuple(card_position.column - 2 for card_position in col)
        data.append(columns)
    return data

def get_all_data(id):
    # get all data and create a dataframe with these columns: round | user | card | position
    study = Study.query.get(id)
    rounds = study.rounds
    data = []
    for round in rounds:
        responses = round.responses
        for response in responses:
            positions = response.positions
            for position in positions:
                data.append([round.id, response.respondent_id, position.card_id, position.column - 2])

    data = pd.DataFrame(data, columns=['round', 'participant', 'card', 'position'])

    return data


def loader_user(user_id):
    return User.query.get(user_id)