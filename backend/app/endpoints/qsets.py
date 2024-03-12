from flask import Blueprint
from flask import jsonify
from app import db
from app.models import QSet
from flask import request

qsets_blueprint = Blueprint('qsets', __name__)

@qsets_blueprint.route('/qsets', methods=['POST'])
def create_qset():
    data = request.get_json()
    new_qset = QSet(title=data['title'], description=data['description'], creator_id=data['creator_id'])
    db.session.add(new_qset)
    db.session.commit()
    return jsonify({'id': new_qset.id,
                    'title': new_qset.title,
                    'description': new_qset.description, 
                    'creator_id': new_qset.creator_id,
                    'cards_count': 0
                    })

@qsets_blueprint.route('/qsets', methods=['GET'])
def get_qsets():
    qsets = QSet.query.all()
    qset_list = [{'id': qset.id, 
                   'title': qset.title, 
                   'description': qset.description, 
                   'creator_id': qset.creator_id, 
                   'cards_count': len(qset.cards)} for qset in qsets]
    return jsonify(qset_list)

@qsets_blueprint.route('/qsets/<int:id>', methods=['GET'])
def get_qset(id):
    qset = db.session.get(QSet, id)
    return jsonify({'id': qset.id, 'title': qset.title, 'description': qset.description, 
                     'creator_id': qset.creator_id, 
                     'cards_count': len(qset.cards),
                     'cards': [{'id': card.id, 'text': card.text} for card in qset.cards]})


