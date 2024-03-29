from flask import Blueprint
from flask import request, jsonify
from app import db
from app.models import Response, CardPosition, Round, User
from datetime import datetime
import json
import numpy as np

responses_blueprint = Blueprint('responses', __name__)


@responses_blueprint.route('/responses', methods=['POST'])
def add_response():
    data = request.get_json()
    new_response = Response(respondent_id=data['respondent_id'],
                            round_id=data['round_id'],
                            time_submitted=datetime.now())
    db.session.add(new_response)
    db.session.commit()
    return jsonify({'id': new_response.id, 'respondent_id': new_response.respondent_id, 
                     'round_id': new_response.round_id, 'time_submitted': new_response.time_submitted})

@responses_blueprint.route('/responses', methods=['GET'])
def get_responses():
    round_id = request.args.get('round')

    if round_id:
        responses = Response.query.filter_by(round_id=round_id).all()
    else:
        responses = Response.query.all()

    responses_list = [{'id': response.id, 'respondent_id': response.respondent_id, 
                     'round_id': response.round_id, 'time_submitted': response.time_submitted,
                    #  join maybe better
                     'user': db.session.get(User, response.respondent_id).name
                     
                     } 
                     for response in responses]
    return jsonify(responses_list)

@responses_blueprint.route('/responses/<int:id>/cards', methods=['POST'])
def add_cards(id):
    data = request.get_json()
    response = db.session.get(Response, id)
    for card in data['cards']:
        position = CardPosition(card_id=card['id'],
                                response_id=response.id,
                                column=card['column'],
                                row=card['row'])
        db.session.add(position)
    db.session.commit()
    return jsonify(data['cards'])


@responses_blueprint.route('/responses/<int:id>/cards', methods=['GET'])
def get_cards(id):
    cards = CardPosition.query.filter_by(response_id=id).order_by(CardPosition.column, CardPosition.row).all()
    distribution = json.loads(db.session.get(Round, db.session.get(Response, id).round_id).study.distribution)
    cumul_distribution = np.cumsum(distribution)
    # prepend 0 to cumul_distribution
    cumul_distribution = np.insert(cumul_distribution, 0, 0)
    cards_return = []
    for count, start_index in zip(distribution, cumul_distribution):
        # append cards in range
        selected = [card.card_id for card in cards[int(start_index):int(start_index + count)]]
        cards_return.append(selected)
    return jsonify(cards_return)