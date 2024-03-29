from flask import Blueprint
from flask import request, jsonify
from app.models import User, Study
from app import db
from flask_login import login_user, logout_user

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], role=data['role'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'role': new_user.role})

@users_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})

@users_blueprint.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    user = db.session.get(User, id)
    data = request.get_json()
    for key in data:
        setattr(user, key, data[key])
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})

@users_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})

@users_blueprint.route('/users', methods=['GET'])
def get_users():
    study_id = request.args.get('studyId')
    if study_id:
        # Return all users ids in a study
        users = Study.query.filter_by(id=study_id).first().users
    else:
        # Return all users
        users = User.query.all()
    
    # Convert users to JSON format
    users_json = [{'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role} for user in users]
    
    return jsonify(users_json)

@users_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], password=data['password'], role='researcher')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'role': new_user.role})

@users_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user.password == data['password']:

        login_user(user)
    
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})


@users_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return "Logged out"