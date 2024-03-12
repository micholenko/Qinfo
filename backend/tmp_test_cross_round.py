from app.models import Card, Response, User, Study
from app import app, db
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_card_matrix(id):
    cards = Card.query.filter_by(qset_id=1).all()
    responses = Response.query.filter_by(round_id=id).all()
    card_positions = []
    for response in responses:
        card_positions.extend(response.positions)

    data = []
    for card in cards:
        col = [
            card_position for card_position in card_positions if card_position.card == card]
        columns = tuple(card_position.column - 2 for card_position in col)
        data.append(columns)
    return data


with app.app_context():
    # get users of a study
    rounds = db.session.query(Study).filter_by(id=1).first().rounds
    data = []
    for i, round in enumerate(rounds):
        round = get_card_matrix(round.id)
        df_round = pd.DataFrame(round)
        df_round = df_round.stack().reset_index()
        df_round = df_round.drop(columns='level_1')

        # rename columns level_0 to card and 0 to position
        df_round.columns = ['card', 'position']

        df_round['round'] = i
        df_round['card'] = df_round['card'].apply(lambda x: Card.query.filter_by(id=x+1).first().text)  
        data.append(df_round)

    data = pd.concat(data)
    print(data)

    fig = px.box(data, x='card', y='position', color='round')
    fig.show()
