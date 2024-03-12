from flask import Blueprint

rounds_blueprint = Blueprint('rounds', __name__)

from app import db
from app.models import StudyRound, User, Card
from flask import jsonify
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from factor_analyzer import Rotator

from app.helpers import get_card_matrix



@rounds_blueprint.route('/rounds/<int:id>/matrix', methods=['GET'])
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

@rounds_blueprint.route('/rounds/<int:id>/factors', methods=['GET'])
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
    print(fig)
    # fig.show()
    
    fig_json = json.loads(fig.to_json())

    ret = {'loadings': np.round(factor_loadings, 4).tolist(), 'eigen': eigen.tolist(), 'scree': fig_json}

    return ret
    return {}

@rounds_blueprint.route('/rounds/<int:id>/rotated_factors', methods=['GET'])
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



@rounds_blueprint.route('/rounds/<int:id>/composite', methods=['GET'])
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
    cards = Card.query.filter_by(qset_id=1).all()
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
