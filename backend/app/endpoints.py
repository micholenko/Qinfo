from app import app, db
from app.models import Study, CardPosition, Response, Card, QSet, User, StudyRound
from flask import request, jsonify
from datetime import datetime, timedelta
import json
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from factor_analyzer import FactorAnalyzer

from app.helpers import get_card_matrix, get_user_rounds
from factor_analyzer import FactorAnalyzer, Rotator


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


@app.route('/studies/<int:id>/user_correlations', methods=['GET'])
def get_user_correlation(id):
    users = db.session.query(Study).filter_by(id=id).first().users
    all_correlations = []
    for user in users:
        data = get_user_rounds(user.id)
        correlation_matrix = np.corrcoef(data, rowvar=False)
        correlations = []
        for i in range(correlation_matrix.shape[0]):
            for j in range(i + 1, correlation_matrix.shape[1]):
                correlations.append(correlation_matrix[i, j])
                print("Round ", i, " and Round ", j, " are correlated", [correlation_matrix[i, j]])
        all_correlations.append(correlations)

    # Create a DataFrame with users and their correlations
    df = pd.DataFrame({
        'user': [user.name for user in users for _ in range(len(all_correlations[0]))],
        'correlation': [corr for correlations in all_correlations for corr in correlations]
    })

    df['count'] = df.groupby(['user', 'correlation'])['user'].transform('count')
    print(df)

    # Create the scatter plot
    fig = px.scatter(df, x='user', y='correlation', size='count', color='correlation',
                     color_continuous_scale=["red", "grey", "green"], range_color=[-1,1],
                     title='User Correlations')
    
    fig.update_yaxes(range=[-1.2, 1.2])
    fig.update_layout(coloraxis_showscale=False)

    scatter = json.loads(fig.to_json())

    fig = px.histogram(df, x='correlation', nbins=20, title='Distribution of Correlations')
    fig.update_xaxes(range=[-1.2, 1.2], nticks=20)
    
    fig.update_xaxes(
        tickvals=[i / 10.0 for i in range(-10, 11)],
        ticktext=[str(i / 10.0) for i in range(-10, 11)]
    )
    fig.update_layout(bargap=0.1)
    # Show the plot
    histogram = json.loads(fig.to_json())

    return jsonify({'scatter': scatter, 'histogram': histogram})

@app.route('/studies/<int:id>/cards_stats', methods=['GET'])
def get_card_stats(id):
    rounds = db.session.query(Study).filter_by(id=id).first().rounds
    data = []
    for i, round in enumerate(rounds):
        round = get_card_matrix(round.id)
        df_round = pd.DataFrame(round)
        df_round = df_round.stack().reset_index()
        df_round = df_round.drop(columns='level_1')

        df_round.columns = ['card', 'position']

        df_round['round'] = i + 1
        df_round['card'] = df_round['card'].apply(lambda x: Card.query.filter_by(id=x+1).first().text)  
        data.append(df_round)

    data = pd.concat(data)
    print(data)

    fig = px.box(data, x='card', y='position', color='round')

    return json.loads(fig.to_json())

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
    print(data)

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

    num_components = 8
    data=np.array(data)

    X = np.array(data)
    standardized_matrix = (data - np.mean(data, axis=0)) / np.std(X, axis=0)

    # Step 4: Correlation Matrix
    correlation_matrix = np.corrcoef(standardized_matrix, rowvar=False)

    # Step 5: Eigenvalue Decomposition
    eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)
    for i in range(num_components):
        if eigenvectors[np.argmax(np.abs(eigenvectors[:, i])), i] < 0:
            eigenvectors[:, i] = -eigenvectors[:, i]

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]


    # Selecting the top 'num_components' eigenvectors
    selected_eigenvectors = sorted_eigenvectors[:, :num_components]

    # Calculate factor loadings
    factor_loadings = selected_eigenvectors * np.sqrt(sorted_eigenvalues[:num_components])



    explained_variance = sorted_eigenvalues / sum(sorted_eigenvalues)

    eigen = np.vstack((sorted_eigenvalues, explained_variance))
    eigen = np.round(eigen, 4)
    eigen = np.column_stack((['eigenvalues', 'explained_variance'], eigen))

    
    fig = px.line(x=[i for i in range(1, len(sorted_eigenvalues[:num_components]) + 1)], 
                  y=sorted_eigenvalues[:num_components], title='Scree Plot', markers=True)
    
    fig_json = json.loads(fig.to_json())

    ret = {'loadings': np.round(factor_loadings, 4).tolist(), 'eigen': eigen.tolist(), 'scree': fig_json}

    return ret



@app.route('/rounds/<int:id>/rotated_factors', methods=['GET'])
def get_rotated_factors(id):
    # im lazy 
    max_components = 8
    data = get_card_matrix(id)
    users = User.query.filter(User.name.like('user%')).all()

    data = np.array(data)

    X = np.array(data)

    # Step 4: Correlation Matrix
    correlation_matrix = np.corrcoef(X, rowvar=False)

    # Step 5: Eigenvalue Decomposition
    eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)

    # go through each column and switch sign if the value with the highest absolute value is negative
    for i in range(eigenvectors.shape[1]):
        if eigenvectors[np.argmax(np.abs(eigenvectors[:, i])), i] < 0:
            eigenvectors[:, i] = -eigenvectors[:, i]

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Selecting the top 'num_components' eigenvectors
    selected_eigenvectors = sorted_eigenvectors[:, :max_components]
    selected_eigenvalues = sorted_eigenvalues[:max_components]

    # Calculate factor loadings
    factor_loadings = selected_eigenvectors * np.sqrt(selected_eigenvalues)


    print(factor_loadings)
    rotator = Rotator()
    rotated_factor_loadings = rotator.fit_transform(factor_loadings[:, :5])
    # round to 2 decimal places
    rotated_factor_loadings = np.round(rotated_factor_loadings, 4)

    return jsonify(rotated_factor_loadings.tolist())



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
    num_components = 5

    # Step 5: Eigenvalue Decomposition
    eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)
    for i in range(num_components):
        if eigenvectors[np.argmax(np.abs(eigenvectors[:, i])), i] < 0:
            eigenvectors[:, i] = -eigenvectors[:, i]

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

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

@app.route('/users', methods=['GET'])
def get_users():
    study_id = request.args.get('studyId')
    if study_id:
        # Return all users of a particular study
        users = Study.query.filter_by(id=study_id).first().users
    else:
        # Return all users
        users = User.query.all()
    
    # Convert users to JSON format
    users_json = [{'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role} for user in users]
    
    return jsonify(users_json)
