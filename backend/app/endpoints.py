from app import app, db
from app.models import Study, CardPosition, Response, Card, QSet, User, StudyRound
from flask import request, jsonify
from datetime import datetime, timedelta
import sys
import json
import pandas as pd
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import plotly.express as px
from factor_analyzer import FactorAnalyzer

from app.helpers import get_card_matrix


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
                     'submit_time': study.submit_time, 'status': study.status, 'q_set_id': study.q_set_id
                     }
                     for study in studies]
    return jsonify(studies_list)


@app.route('/studies/<int:id>', methods=['GET'])
def get_study(id):
    study = db.session.get(Study, id)
    return jsonify({'id': study.id, 'title': study.title, 'question': study.question, 
                     'description': study.description, 'created_time': study.created_time,
                     'submit_time': study.submit_time, 'status': study.status, 'q_set_id': study.q_set_id,
                     'rounds': {'count': len(study.rounds), 'ids': [round.id for round in study.rounds]},
                     'distribution': json.loads(study.distribution) if study.distribution else None,

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

@app.route('/qsets/<int:id>', methods=['GET'])
def get_qset(id):
    qset = db.session.get(QSet, id)
    return jsonify({'id': qset.id, 'title': qset.title, 'description': qset.description, 
                     'creator_id': qset.creator_id, 
                     'cards_count': len(qset.cards),
                     'cards': [{'id': card.id, 'text': card.text} for card in qset.cards]})


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
                     'round_id': response.round_id, 'time_submitted': response.time_submitted,
                    #  join maybe better
                     'user': db.session.get(User, response.respondent_id).name
                     
                     } 
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
    cards = CardPosition.query.filter_by(response_id=id).order_by(CardPosition.column, CardPosition.row).all()
    distribution = json.loads(db.session.get(StudyRound, db.session.get(Response, id).round_id).study.distribution)
    cumul_distribution = np.cumsum(distribution)
    # prepend 0 to cumul_distribution
    cumul_distribution = np.insert(cumul_distribution, 0, 0)
    cards_return = []
    for count, start_index in zip(distribution, cumul_distribution):
        # append cards in range
        selected = [card.card_id for card in cards[int(start_index):int(start_index + count)]]
        cards_return.append(selected)
    return jsonify(cards_return)


@app.route('/rounds/<int:id>/matrix', methods=['GET'])
def get_matrix(id):
    data = get_card_matrix(id)

    # print all users starting with "user"
    users = User.query.filter(User.name.like('user%')).all()
    df = pd.DataFrame(data, columns=[user.name for user in users])
    matrix = df.corr(method='pearson')    

    fig = go.Figure(data=go.Heatmap(
                z=matrix,
                x=list(matrix.columns),
                y=list(matrix.index),
                colorscale='Viridis',
                zmin=-1, zmax=1))

    annotations = []
    for i, row in enumerate(matrix.values):
        for j, value in enumerate(row):
            annotations.append(go.layout.Annotation(text=str(value.round(2)), x=matrix.columns[j], y=matrix.index[i], showarrow=False))

    fig.update_layout(
        annotations=annotations,
        xaxis=dict(side="top")
        )
    fig.update_yaxes(autorange="reversed")
    # fig.show()
    return fig.to_json()

@app.route('/rounds/<int:id>/factors', methods=['GET'])
def get_factors(id):
    data = get_card_matrix(id)
    users = User.query.filter(User.name.like('user%')).all()

    data=np.array(data)

    X = np.array(data)
    standardized_matrix = (data - np.mean(data, axis=0)) / np.std(X, axis=0)

    # Step 4: Correlation Matrix
    correlation_matrix = np.corrcoef(standardized_matrix, rowvar=False)
    print('corr')
    print(correlation_matrix.round(2))

    # Step 5: Eigenvalue Decomposition
    eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    print('eigenvalues')
    print(np.round(sorted_eigenvalues, 4))

    num_components = 5

    # Selecting the top 'num_components' eigenvectors
    selected_eigenvectors = sorted_eigenvectors[:, :num_components]

    # Calculate factor loadings
    factor_loadings = selected_eigenvectors * np.sqrt(sorted_eigenvalues[:num_components])

    # Create a factor loadings table
    factor_loadings_table = np.column_stack((np.arange(1, X.shape[1] + 1), factor_loadings))
    print('loadings')
    print(np.round(factor_loadings_table, 4))

    explained_variance = sorted_eigenvalues / sum(sorted_eigenvalues)
    print('explained variance')
    print(np.round(explained_variance, 4))

    eigen = np.vstack((sorted_eigenvalues, explained_variance))
    eigen = np.round(eigen, 4)
    eigen = np.column_stack((['eigenvalues', 'explained_variance'], eigen))

    
    fig = px.line(x=[i for i in range(1, len(sorted_eigenvalues[:num_components]) + 1)], 
                  y=sorted_eigenvalues[:num_components], title='Scree Plot', markers=True)
    
    fig_json = json.loads(fig.to_json())

    ret = {'loadings': np.round(factor_loadings_table, 2).tolist(), 'eigen': eigen.tolist(), 'scree': fig_json}

    

    return ret



@app.route('/rounds/<int:id>/rotated_factors', methods=['GET'])
def get_rotated_factors(id):
    pass
    # rotate with varimax
    # varimax = FactorAnalyzer(rotation='varimax')
    # varimax.fit(data)


@app.route('/rounds/<int:id>/composite')
def get_composite_qsorts(id):

# im lazy 
    data = get_card_matrix(id)
    users = User.query.filter(User.name.like('user%')).all()

    data=np.array(data)

    X = np.array(data)
    standardized_matrix = (data - np.mean(data, axis=0)) / np.std(X, axis=0)

    # Step 4: Correlation Matrix
    correlation_matrix = np.corrcoef(standardized_matrix, rowvar=False)
    print('corr')
    print(correlation_matrix.round(2))

    # Step 5: Eigenvalue Decomposition
    eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    num_components = 5

    # Selecting the top 'num_components' eigenvectors
    selected_eigenvectors = sorted_eigenvectors[:, :num_components]


#  end of im lazy
    factor_scores = np.dot(standardized_matrix, selected_eigenvectors)
    # Display factor scores
    print("Factor Scores:")
    print(factor_scores)

    # get distribution from study 
    distribution = json.loads(db.session.get(StudyRound, id).study.distribution)
    cumul_distribution = np.cumsum(distribution)
    cumul_distribution = np.insert(cumul_distribution, 0, 0)

    print(cumul_distribution)
    # get cards
    cards = Card.query.filter_by(qSet_id=1).all()
    print(cards)

    q_sorts = np.argsort(-factor_scores, axis=0)
    q_sorts = q_sorts[::-1].T


    data = []
    for i, q_sort in enumerate(q_sorts):
        qsort = {
            'id': i,
            'cards': []
        }
        sort = []
        for count, start_index in zip(distribution, cumul_distribution):
            # append cards in range
            selected = [cards[i].id for i in q_sort[int(start_index):int(start_index + count)]]
            print(selected)
            sort.append(selected)
        qsort['cards'] = sort
        data.append(qsort)

    return jsonify(data)