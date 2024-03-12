from flask import Blueprint
from flask import request, jsonify
from app import db
from app.models import Study, CardPosition, Response, Card, QSet, User, StudyRound
from datetime import datetime, timedelta
import json
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from app.helpers import get_card_matrix, get_user_rounds, get_all_data

studies_blueprint = Blueprint('studies', __name__)

@studies_blueprint.route('/studies', methods=['POST'])
def create_study():
    # from request json body
    data = request.get_json()
    new_study = Study(title=data['title'],
                        question=data['question'],
                        description=data['description'],
                        distribution=json.dumps(data['distribution']),
                        col_values=json.dumps(data['col_values']),
                        created_time=datetime.now(),
                        submit_time=datetime.now() + timedelta(days=7),
                        status='not_started',
                        qset_id=data['qset_id'] if 'qset_id' in data else None
                        )
    db.session.add(new_study)
    db.session.commit()
    return jsonify({'id': new_study.id, 'title': new_study.title, 'question': new_study.question, 
                     'description': new_study.description, 'created_time': new_study.created_time,
                     'submit_time': new_study.submit_time, 'status': new_study.status, 'qset_id': new_study.qset_id})

@studies_blueprint.route('/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()
    studies_list = [{'id': study.id, 'title': study.title, 'question': study.question, 
                     'description': study.description, 'created_time': study.created_time,
                     'submit_time': study.submit_time, 'status': study.status, 'qset_id': study.qset_id
                     }
                     for study in studies]
    return jsonify(studies_list)


@studies_blueprint.route('/studies/<int:id>', methods=['GET'])
def get_study(id):
    study = db.session.get(Study, id)
    return jsonify({'id': study.id, 'title': study.title, 'question': study.question, 
                     'description': study.description, 'created_time': study.created_time,
                     'submit_time': study.submit_time, 'status': study.status, 'qset_id': study.qset_id,
                     'rounds': {'count': len(study.rounds), 'ids': [round.id for round in study.rounds]},
                     'distribution': json.loads(study.distribution) if study.distribution else None,
                     'col_values': json.loads(study.col_values) if study.col_values else None
                     })

@studies_blueprint.route('/studies/<int:id>', methods=['PATCH'])
def update_study(id):
    study = db.session.get(Study, id)
    data = request.get_json()
    # update only the fields that are in the request
    print(data)
    for key in data:
        setattr(study, key, data[key])
    db.session.commit()
    return jsonify({'id': study.id, 'title': study.title, 'question': study.question,
                        'description': study.description, 'created_time': study.created_time,
                        'submit_time': study.submit_time, 'status': study.status, 'qset_id': study.qset_id})


@studies_blueprint.route('/studies/<int:id>', methods=['DELETE'])
def delete_study(id):
    study = db.session.get(Study, id)
    db.session.delete(study)
    db.session.commit()
    return "Study deleted"

@studies_blueprint.route('/studies/<int:id>/user_correlations', methods=['GET'])
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

@studies_blueprint.route('/studies/<int:id>/cards_stats', methods=['GET'])
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

@studies_blueprint.route('/studies/<int:id>/data', methods=['GET'])
def get_study_data(id):
    data = get_all_data(id)
    # convert to json array
    # data = data.to_json(orient='records')

    # empty dataframe
    df = pd.DataFrame()

    for i in range(1,4):
        data = get_card_matrix(id)
        data = pd.DataFrame(data)
        # append to df 
        # add column round
        #transpose data
        data = data.T
        data['round'] = i
        data['id'] = range(0, len(data))
        df = pd.concat([df, data], axis=0)

    
    # dont apply to round column
    round_col = df['round']
    id_col = df['id']
    df = df.drop(columns=['round'])
    df = df.drop(columns=['id'])

    scaler = StandardScaler()
    data = scaler.fit_transform(df)

    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(data)

    principal_df = pd.DataFrame(data=principalComponents, columns=['principal component 1', 'principal component 2', 'principal component 3'])
    # reset index to match round column
    round_col = round_col.reset_index(drop=True)
    id_col = id_col.reset_index(drop=True)
    


    # group by principal components and count, aggregate and add column count
    # principal_df = principal_df.groupby(['principal component 1', 'principal component 2']).size().reset_index(name='count')
    principal_df['round'] = round_col
    principal_df['id'] = id_col

    # jitter principal components
    principal_df['principal component 1'] = principal_df['principal component 1'] + np.random.normal(0, 0.1, len(principal_df))
    principal_df['principal component 2'] = principal_df['principal component 2'] + np.random.normal(0, 0.1, len(principal_df))
    principal_df['principal component 3'] = principal_df['principal component 3'] + np.random.normal(0, 0.1, len(principal_df))


    # increase the size of the points
    fig = px.scatter_3d(principal_df, x='principal component 1', y='principal component 2', z='principal component 3', color='round', size_max=18, opacity=0.7, title='3D PCA')
    fig.update_traces(marker=dict(size=12, opacity=0.8))


    fig.show()

    return data




