from app import app, db
from app.models import Study, CardPosition, Response, Card
from flask import request, jsonify
from datetime import datetime, timedelta
import sys
import json


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello, World!" 

# post reqeust to create a study
@app.route('/studies', methods=['POST'])
def create_study():
    # from request json body
    data = request.get_json()
    new_study = Study(title=data['title'],
                        question=data['question'],
                        description=data['description'],
                        created_time=datetime.now(),
                        submit_time=datetime.now() + timedelta(days=7),
                        status='not_started',
                        q_set_id=data['q_set_id'] if 'q_set_id' in data else None
                        )
    db.session.add(new_study)
    db.session.commit()
    return jsonify({'id': new_study.id, 'title': new_study.title, 'question': new_study.question, 
                     'description': new_study.description, 'created_time': new_study.created_time,
                     'submit_time': new_study.submit_time, 'status': new_study.status, 'q_set_id': new_study.q_set_id})

@app.route('/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()
    studies_list = [{'id': study.id, 'title': study.title, 'question': study.question, 
                     'description': study.description, 'created_time': study.created_time,
                     'submit_time': study.submit_time, 'status': study.status, 'q_set_id': study.q_set_id} 
                     for study in studies]
    return jsonify(studies_list)


@app.route('/studies/<int:id>', methods=['GET'])
def get_study(id):
    study = db.session.get(Study, id)
    return jsonify({'id': study.id, 'title': study.title, 'question': study.question, 
                     'description': study.description, 'created_time': study.created_time,
                     'submit_time': study.submit_time, 'status': study.status, 'q_set_id': study.q_set_id,
                     'rounds': {'count': len(study.rounds), 'ids': [round.id for round in study.rounds]},
                     'distribution': json.loads(study.distribution) if study.distribution else None
                     })

@app.route('/studies/<int:id>', methods=['PUT'])
def update_study(id):
    study = db.session.get(Study, id)
    data = request.get_json()
    study.title = data['title']
    study.question = data['question']
    study.description = data['description']
    study.created_time = data['created_time']
    study.submit_time = data['submit_time']
    study.status = data['status']
    study.q_set_id = data['q_set_id']
    db.session.commit()
    return jsonify({'id': study.id, 'title': study.title, 'question': study.question, 
                     'description': study.description, 'created_time': study.created_time,
                     'submit_time': study.submit_time, 'status': study.status, 'q_set_id': study.q_set_id})

@app.route('/studies/<int:id>', methods=['DELETE'])
def delete_study(id):
    study = db.session.get(Study, id)
    db.session.delete(study)
    db.session.commit()
    return "Study deleted"


@app.route('/responses', methods=['POST'])
def add_response():
    data = request.get_json()
    new_response = Response(respondent_id=data['respondent_id'],
                            round_id=data['round_id'],
                            time_submitted=datetime.now())
    db.session.add(new_response)
    db.session.commit()
    return jsonify({'id': new_response.id, 'respondent_id': new_response.respondent_id, 
                     'round_id': new_response.round_id, 'time_submitted': new_response.time_submitted})

@app.route('/responses', methods=['GET'])
def get_responses():
    round_id = request.args.get('round')
    if round_id:
        responses = Response.query.filter_by(round_id=round_id).all()
    else:
        responses = Response.query.all()

    print(responses)
    responses_list = [{'id': response.id, 'respondent_id': response.respondent_id, 
                     'round_id': response.round_id, 'time_submitted': response.time_submitted} 
                     for response in responses]
    return jsonify(responses_list)

@app.route('/responses/<int:id>/cards', methods=['POST'])
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


@app.route('/responses/<int:id>/cards', methods=['GET'])
def get_cards(id):
    # ordering is implicit
    print(id)
    cards = CardPosition.query.filter_by(response_id=id).order_by(CardPosition.column, CardPosition.row).all()
    print(cards)
    response = db.session.get(Response, id)
    cards_return = [{'id': card.card_id, 'column': card.column, 'row': card.row} for card in cards]
    # group concat???
    
    return jsonify(cards_return)