from flask import Blueprint
from flask import request, jsonify
from app import db
from app.models import Card

cards_blueprint = Blueprint('cards', __name__)

# TODO: probably remove and add functionality to qsets, or idk

@cards_blueprint.route('/cards', methods=['POST'])
def create_card():
    data = request.get_json()
    new_card = Card(text=data['text'], qset_id=data['qset_id'], creator_id=data['creator_id'])
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'id': new_card.id, 'text': new_card.text, 'qset_id': new_card.qset_id})

@cards_blueprint.route('/cards/<int:id>', methods=['GET'])
def get_card(id):
    card = db.session.get(Card, id)
    return jsonify({'id': card.id, 'text': card.text, 'qset_id': card.qset_id})

@cards_blueprint.route('/cards', methods=['GET'])
def get_cards():
    qset_id = request.args.get('qset_id')
    if qset_id:
        cards = Card.query.filter_by(qset_id=qset_id).all()
    else:
        cards = Card.query.all()
    cards_list = [{'id': card.id, 'text': card.text, 'qset_id': card.qset_id} for card in cards]
    return jsonify(cards_list)

@cards_blueprint.route('/cards/<int:id>', methods=['PATCH'])
def update_card(id):
    card = db.session.get(Card, id)
    data = request.get_json()
    for key in data:
        setattr(card, key, data[key])
    db.session.commit()
    return jsonify({'id': card.id, 'text': card.text, 'qset_id': card.qset_id})

@cards_blueprint.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    card = db.session.get(Card, id)
    db.session.delete(card)
    db.session.commit()
    return "Card deleted successfully"


