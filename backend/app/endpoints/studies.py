from flask import Blueprint
from flask import request, jsonify
from app import db
from app.models import Study, CardPosition, Response, Card, QSet, User, Round
from datetime import datetime, timedelta
import json
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.spatial.distance import euclidean
from itertools import combinations
import plotly.graph_objects as go

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
                      status='not_started',
                      qset_id=data['qset_id'] if 'qset_id' in data else None
                      )
    db.session.add(new_study)
    db.session.commit()
    return jsonify({'id': new_study.id, 'title': new_study.title, 'question': new_study.question,
                    'description': new_study.description, 'created_time': new_study.created_time,
                    'status': new_study.status, 'qset_id': new_study.qset_id})


@studies_blueprint.route('/studies', methods=['GET'])
def get_studies():
    studies = Study.query.all()
    studies_list = [{'id': study.id, 'title': study.title, 'question': study.question,
                     'description': study.description, 'created_time': study.created_time,
                     'rounds': {'count': len(study.rounds), 'ids': [round.id for round in study.rounds]},
                     'participants': {'count': len(study.users), 'ids': [user.id for user in study.users]},
                     'cards': {'count': len(study.qset.cards), 'ids': [card.id for card in study.qset.cards]},
                     'status': study.status, 'qset_id': study.qset_id
                     }
                    for study in studies]
    return jsonify(studies_list)


@studies_blueprint.route('/studies/<int:id>', methods=['GET'])
def get_study(id):
    study = db.session.get(Study, id)
    return jsonify({'id': study.id, 'title': study.title, 'question': study.question,
                    'description': study.description, 'created_time': study.created_time,
                    'status': study.status, 'qset_id': study.qset_id,
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
                    'status': study.status, 'qset_id': study.qset_id})


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
                print("Round ", i, " and Round ", j,
                      " are correlated", [correlation_matrix[i, j]])
        all_correlations.append(correlations)

    # Create a DataFrame with users and their correlations
    df = pd.DataFrame({
        'user': [user.name for user in users for _ in range(len(all_correlations[0]))],
        'correlation': [corr for correlations in all_correlations for corr in correlations]
    })

    df['count'] = df.groupby(['user', 'correlation'])[
        'user'].transform('count')
    print(df)

    # Create the scatter plot
    fig = px.scatter(df, x='user', y='correlation', size='count', color='correlation',
                     color_continuous_scale=["red", "grey", "green"], range_color=[-1, 1],
                     title='User Correlations')

    fig.update_yaxes(range=[-1.2, 1.2])
    fig.update_layout(coloraxis_showscale=False)

    scatter = json.loads(fig.to_json())

    fig = px.histogram(df, x='correlation', nbins=20,
                       title='Distribution of Correlations')
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
    study = db.session.query(Study).filter_by(id=id).first()
    rounds = study.rounds
    data = []
    for i, round in enumerate(rounds):
        round = get_card_matrix(round, study)
        df_round = pd.DataFrame(round)
        df_round = df_round.stack().reset_index()
        df_round = df_round.drop(columns='level_1')

        df_round.columns = ['card', 'position']

        df_round['round'] = i + 1
        df_round['card'] = df_round['card'].apply(
            lambda x: Card.query.filter_by(id=x+1).first().text)
        data.append(df_round)

    data = pd.concat(data)

    fig = px.box(data, x='card', y='position', color='round')

    return json.loads(fig.to_json())


@studies_blueprint.route('/studies/<int:id>/data', methods=['GET'])
def get_study_data(id):
    data = get_all_data(id)
    # convert to json array
    data = data.to_json(orient='records')
    return data


@studies_blueprint.route('/studies/<int:id>/users_pca', methods=['GET'])
def get_study_users(id):
    df = pd.DataFrame()
    users = db.session.query(Study).filter_by(id=id).first().users
    study = db.session.query(Study).filter_by(id=id).first()
    for round in study.rounds:
        data = get_card_matrix(round, study)
        data = pd.DataFrame(data)
        # append to df
        # add column round
        # transpose data
        data = data.T
        # data['round'] = i
        # data['id'] = [user.id for user in users]
        df = pd.concat([df, data], axis=1)

    # dont apply to round column

    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(df)

    principal_df = pd.DataFrame(data=principalComponents, columns=[
                                'PC1', 'PC2', 'PC3'])
    # reset index to match round column

    # group by principal components and count, aggregate and add column count
    # principal_df = principal_df.groupby(['PC1', 'PC2']).size().reset_index(name='count')
    # for each row map the user id to the user name

    principal_df['id'] = [user.id for user in users]
    principal_df['user_name'] = principal_df['id'].apply(
        lambda x: db.session.get(User, x).name)

    # jitter principal components
    principal_df['PC1'] = principal_df['PC1'] + \
        np.random.normal(0, 0.1, len(principal_df))
    principal_df['PC2'] = principal_df['PC2'] + \
        np.random.normal(0, 0.1, len(principal_df))
    principal_df['PC3'] = principal_df['PC3'] + \
        np.random.normal(0, 0.1, len(principal_df))

    


    fig = px.scatter_3d(principal_df, x='PC1', y='PC2',
                        z='PC3', size_max=18, opacity=0.7,
                        hover_data={'PC1': False, 'PC2': False,
                                    'PC3': False, 'user_name': True},
                        custom_data=['id', 'user_name'],
                        )
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_traces(
        hovertemplate='<b>%{customdata[1]}</b><br>Click to see details')

    return json.loads(fig.to_json())


@studies_blueprint.route('/studies/<int:id>/average_euclidean_distance', methods=['GET'])
def get_average_euclidean_distance(id):
    df = pd.DataFrame()

    study = db.session.query(Study).filter_by(id=id).first()

    for i in study.rounds:
        data = get_card_matrix(i, study)
        data = pd.DataFrame(data)
        # append to df
        # add column round
        # transpose data
        data = data.T
        data['round'] = i
        data['id'] = range(0, len(data))
        df = pd.concat([df, data], axis=0)

    print("start data")
    print(df)

    # dont apply to round column
    round_col = df['round']
    id_col = df['id']
    df = df.drop(columns=['round'])
    df = df.drop(columns=['id'])

    scaler = StandardScaler()
    data = scaler.fit_transform(df)

    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(data)

    principal_df = pd.DataFrame(data=principalComponents, columns=[
                                'PC1', 'PC2', 'PC3'])
    # reset index to match round column
    round_col = round_col.reset_index(drop=True)
    id_col = id_col.reset_index(drop=True)

    # group by principal components and count, aggregate and add column count
    # principal_df = principal_df.groupby(['PC1', 'PC2']).size().reset_index(name='count')
    principal_df['round'] = round_col
    principal_df['id'] = id_col

    # jitter principal components
    # principal_df['principal component 1'] = principal_df['principal component 1'] + np.random.normal(0, 0.1, len(principal_df))
    # principal_df['PC2'] = principal_df['PC2'] + np.random.normal(0, 0.1, len(principal_df))
    # principal_df['PC3'] = principal_df['PC3'] + np.random.normal(0, 0.1, len(principal_df))

    grouped = principal_df.groupby('id')

    # Function to calculate average Euclidean distance between all combinations of rows within each group

    def average_euclidean_distance(group):
        distances = []
        for pair in combinations(group.values, 2):
            distances.append(euclidean(pair[0][:-2], pair[1][:-2]))
        return sum(distances) / len(distances)

    # Apply the function to each group and calculate average distances}
    average_distances = grouped.apply(average_euclidean_distance)

    # get users of a study
    # add user names to the average_distances
    users = db.session.query(Study).filter_by(id=id).first().users

    # add column with the value 1
    average_distances = average_distances.to_frame(name='distance')
    # add round column as a category
    average_distances['user_ids'] = [user.id for user in users]
    average_distances['user_names'] = [user.name for user in users]
    average_distances['pos'] = 1


    # jitter pos 
    average_distances['pos'] = average_distances['pos'] + \
        np.random.normal(0, 0.05, len(average_distances))


    # add name column, lookup user by id



    fig2 = px.scatter(average_distances, x='pos', y='distance',
                      hover_name='user_names',
                      hover_data={'user_ids': False,
                                  'distance': False, 'pos': False},
                      color='distance',
                      color_continuous_scale=px.colors.diverging.RdYlGn_r,
                      range_color=[0, max(average_distances['distance'])],
                      custom_data=['user_ids', 'user_names'],
                      )

    # add styling to selected points

    fig2.update_traces(marker=dict(size=14, opacity=0.8,
                       line=dict(width=1, color='DarkSlateGrey')))
    fig2.update_traces(
        hovertemplate='<b>%{customdata[1]}</b><br>Click to see details')

    # show x labels on the bottom
    fig2.update_xaxes(side='bottom', showticklabels=False)
    fig2.update_xaxes(title=None)
    fig2.update_yaxes(title='Average Euclidean Distance')

    # type "inconsistent" on the top of the y axis
    fig2.add_annotation(x=0.5, y=0.99, xref='paper', yref='paper',
                        text='Inconsistent', showarrow=False,
                        font=dict(size=16, color='black'))
    fig2.add_annotation(x=0.5, y=0.01, xref='paper', yref='paper',
                        text='Consistent', showarrow=False,
                        font=dict(size=16, color='black'))
    # show y axis from 0 to max distance
    max_distance = max(average_distances['distance'])
    fig2.update_yaxes(range=[ -0.05 if max_distance < 1 else -0.5, max_distance + 0.5])
    # remove the colorbar
    fig2.update_layout(coloraxis_showscale=False)

    return json.loads(fig2.to_json())


@studies_blueprint.route('/studies/<int:id>/user_details', methods=['GET'])
def get_user_details(id):
    user_id = request.args.get('user_id')
    data = get_user_rounds(id, user_id)
    # create correlation matrix for the user
    print(data)
    correlation_matrix = np.corrcoef(data, rowvar=False)
    print(correlation_matrix)
    fig = px.imshow(correlation_matrix, color_continuous_scale='Viridis')
    fig.update_layout(title='User Correlation Matrix')
    # remove the colorbar
    fig.update_layout(coloraxis_showscale=False)
    # add numbers to the heatmap
    fig.update_layout(annotations=[])
    # add the numbers to each cell of the heatmap
    for i in range(correlation_matrix.shape[0]):
        for j in range(correlation_matrix.shape[1]):
            fig.add_annotation(
                x=j,
                y=i,
                text=str(round(correlation_matrix[i, j], 2)),
                showarrow=False,
                font=dict(color='black')
            )

    # add round labels
    fig.update_xaxes(tickvals=list(range(0, len(correlation_matrix))),
                     ticktext=[f'Round {i+1}' for i in range(len(correlation_matrix))])
    fig.update_yaxes(tickvals=list(range(0, len(correlation_matrix))),
                     ticktext=[f'Round {i+1}' for i in range(len(correlation_matrix))])

    # move x axis to the top
    fig.update_xaxes(side='top')

    return json.loads(fig.to_json())

@studies_blueprint.route('/studies/<int:id>/user_card_stats', methods=['GET'])
def get_user_card_stats(id):
    user_id = request.args.get('user_id')
    study = db.session.query(Study).filter_by(id=id).first()

    data = get_all_data(id)
    print(data)
    print(user_id)
    data = data[data['participant'] == int(user_id)
    ]
    print(data)

    # calculate the mean and standard deviation of each card
    card_stats = data.groupby('card').agg({'position': ['mean', 'std']})
    card_stats.columns = ['mean', 'std']
    card_stats = card_stats.reset_index()
    # create a plot with the mean and standard deviation of each card

    cards = db.session.query(Study).filter_by(id=id).first().qset.cards
    card_stats['id'] = [card.id for card in cards]
    card_stats['name'] = [card.text for card in cards]

    print(card_stats)

    fig = px.scatter(card_stats, x='std', y='mean',
                        custom_data=['id', 'name'])
    
    # set max x and y values
    fig.update_xaxes(range=[-0.2, max(card_stats['std']) + 0.5])

    col_values = json.loads(study.col_values)

    fig.update_yaxes(range=[col_values[0]-0.2, col_values[-1]+0.2])
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_traces(
        hovertemplate='''<b>%{customdata[1]}</b><br><b>Mean:</b> %{y}<br><b>Standard Deviation:</b> %{x}<br>Click to see details''')
    
    fig.update_traces(textposition='top center')

    return json.loads(fig.to_json())

    




@studies_blueprint.route('/studies/<int:id>/card_stats2', methods=['GET'])
def get_study_card_stats(id):
    study = db.session.query(Study).filter_by(id=id).first()
    data = get_all_data(id)
    # calculate the mean and standard deviation of each card
    card_stats = data.groupby('card').agg({'position': ['mean', 'std']})
    card_stats.columns = ['mean', 'std']
    card_stats = card_stats.reset_index()
    # create a plot with the mean and standard deviation of each card

    cards = db.session.query(Study).filter_by(id=id).first().qset.cards
    card_stats['id'] = [card.id for card in cards]
    card_stats['name'] = [card.text for card in cards]

    print(card_stats)

    fig = px.scatter(card_stats, x='std', y='mean',
                     custom_data=['id', 'name'])

    # set max x and y values
    fig.update_xaxes(range=[-0.2, max(card_stats['std']) + 0.5])

    col_values = json.loads(study.col_values)

    fig.update_yaxes(range=[col_values[0]-0.2, col_values[-1]+0.2])
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_traces(
        hovertemplate='''<b>%{customdata[1]}</b><br><b>Mean:</b> %{y}<br><b>Standard Deviation:</b> %{x}<br>Click to see details''')

    fig.update_traces(textposition='top center')

    return json.loads(fig.to_json())


@studies_blueprint.route('/studies/<int:id>/test', methods=['GET'])
def get_per_round_PCA(id):
    df = pd.DataFrame()
    users = db.session.query(Study).filter_by(id=id).first().users

    for i in range(1, 4):
        data = get_card_matrix(i)
        data = pd.DataFrame(data)
        # append to df
        # add column round
        # transpose data
        data = data.T
        data['round'] = i
        data['id'] = [user.id for user in users]
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

    principal_df = pd.DataFrame(data=principalComponents, columns=[
                                'PC1', 'PC2', 'PC3'])
    # reset index to match round column

    round_col = round_col.reset_index(drop=True)
    id_col = id_col.reset_index(drop=True)

    # group by principal components and count, aggregate and add column count
    # principal_df = principal_df.groupby(['PC1', 'PC2']).size().reset_index(name='count')
    principal_df['round'] = round_col
    principal_df['id'] = id_col
    # for each row map the user id to the user name
    principal_df['user_name'] = principal_df['id'].apply(
        lambda x: db.session.get(User, x).name)

    # jitter principal components
    principal_df['PC1'] = principal_df['PC1'] + \
        np.random.normal(0, 0.1, len(principal_df))
    principal_df['PC2'] = principal_df['PC2'] + \
        np.random.normal(0, 0.1, len(principal_df))
    principal_df['PC3'] = principal_df['PC3'] + \
        np.random.normal(0, 0.1, len(principal_df))

    print(principal_df)

    # increase the size of the points
    fig = px.scatter_3d(principal_df, x='PC1', y='PC2',
                        z='PC3', color='round', size_max=18, opacity=0.7, title='3D PCA',
                        hover_data={'PC1': False, 'PC2': False,
                                    'PC3': False, 'user_name': True, 'round': True},
                        )
    fig.update_traces(marker=dict(size=12, opacity=0.8))

    return json.loads(fig.to_json())


@studies_blueprint.route('/studies/<int:id>/cards/<int:card_id>', methods=['GET'])
def get_card_details(id, card_id):
    study = db.session.query(Study).filter_by(id=id).first()
    col_values = json.loads(study.col_values)
    data = get_all_data(id)
    card_data = data[data['card'] == card_id]
    print(card_data)
    import plotly.graph_objects as go

    # map round to round name
    card_data['round'] = card_data['round'].apply(
        lambda x: db.session.get(Round, x).name)


    fig1 = go.Figure()
    fig1.add_trace(go.Box(y=card_data['position'], name='Average'))   
    fig1.add_trace(go.Box(x=card_data['round'], y=card_data['position'], name='Per Round'))

    fig1.update_layout(xaxis_title='Round', yaxis_title='Position')
    fig1.update_yaxes(range=[col_values[0]-0.2, col_values[-1]+0.2])

    fig1.update_layout(showlegend=False)


    # create a scatter plot with mean and standard deviation for each participant
    participant_stats = card_data.groupby('participant').agg(
        {'position': ['mean', 'std']})
    
    participant_stats.columns = ['mean', 'std']
    participant_stats = participant_stats.reset_index()
    participant_stats['participant'] = [db.session.get(User, user_id).name for user_id in participant_stats['participant']]
    print("Participant stats")
    print(participant_stats)

    # create a trace for each participant which has mean and std as x and y

    fig2 = go.Figure()
    for i, participant in enumerate(participant_stats['participant']):
        fig2.add_trace(go.Scatter(x=[participant_stats['std'][i]], y=[participant_stats['mean'][i]], mode='markers', name=participant, marker=dict(size=12, opacity=0.8, color='#6666FF')))

    # show overlapping points on hover
    fig2.update_layout(hovermode='x', hoverdistance=1)
    # fig2.update_traces(marker=dict(size=12, opacity=0.8))
    fig2.update_xaxes(title='Standard Deviation')
    fig2.update_yaxes(title='Mean Position')

    fig2.update_layout(showlegend=False)
    



    return {'cardBoxPlot': json.loads(fig1.to_json()),
            'cardScatterPlot': json.loads(fig2.to_json())}
    
    
@studies_blueprint.route('/studies/<int:id>/rounds_stats', methods=['GET'])
def get_rounds_stats(id):
    # calculate correlation for each round, take the average of the correlation matrix
    study = db.session.query(Study).filter_by(id=id).first()
    rounds = study.rounds
    averages = []
    for round in rounds:
        data = get_card_matrix(round, study)
        users = study.users    
        df = pd.DataFrame(data, columns=[user.name for user in users])
        matrix = df.corr(method='pearson')
        # get average of the correlation matrix
        average = matrix.mean().mean()
        averages.append(average)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[i+1 for i in range(len(averages))], y=averages, mode='markers'))
    fig.update_layout(xaxis_title='Round', yaxis_title='Average Correlation')
    return json.loads(fig.to_json())


@studies_blueprint.route('/studies/<int:id>/rounds/<int:round_id>', methods=['GET'])
def get_round_details(id, round_id):
    # get mean and std scatter plot for each card
    study = db.session.query(Study).filter_by(id=id).first()
    data = get_all_data(id)
    round_data = data[data['round'] == round_id]

    # calculate the mean and standard deviation of each card
    card_stats = round_data.groupby('card').agg({'position': ['mean', 'std']})
    card_stats.columns = ['mean', 'std']
    card_stats = card_stats.reset_index()
    # create a plot with the mean and standard deviation of each card

    cards = db.session.query(Study).filter_by(id=id).first().qset.cards
    card_stats['id'] = [card.id for card in cards]
    card_stats['name'] = [card.text for card in cards]

    fig = px.scatter(card_stats, x='std', y='mean',
                     custom_data=['id', 'name'])

    # set max x and y values
    fig.update_xaxes(range=[-0.2, max(card_stats['std']) + 0.5])

    col_values = json.loads(study.col_values)

    fig.update_yaxes(range=[col_values[0]-0.2, col_values[-1]+0.2])
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_traces(
        hovertemplate='''<b>%{customdata[1]}</b><br><b>Mean:</b> %{y}<br><b>Standard Deviation:</b> %{x}<br>Click to see details''')

    fig.update_traces(textposition='top center')

    return json.loads(fig.to_json())    

