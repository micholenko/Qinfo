from app.models import Card, Response


def get_card_matrix(id):
    cards = Card.query.filter_by(qSet_id=1).all()
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
    cards = Card.query.filter_by(qSet_id=1).all()
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
    cards = Card.query.filter_by(qSet_id=1).all()
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