from app.models import Card, CardPosition


def get_card_matrix(id):
    cards = Card.query.filter_by(qSet_id=1).all()
    print(cards)
    data = []
    for card in cards:
        card_positions = CardPosition.query.filter_by(card_id=card.id).all()
        columns = tuple(card_position.column - 2 for card_position in card_positions)
        print(columns)
        data.append(columns)

    return data