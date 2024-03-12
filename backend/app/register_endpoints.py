from app import app, db
from app.endpoints.studies import studies_blueprint
from app.endpoints.qsets import qsets_blueprint
from app.endpoints.users import users_blueprint
from app.endpoints.responses import responses_blueprint
from app.endpoints.cards import cards_blueprint
from app.endpoints.rounds import rounds_blueprint

app.register_blueprint(studies_blueprint)
app.register_blueprint(qsets_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(responses_blueprint)
app.register_blueprint(cards_blueprint)
app.register_blueprint(rounds_blueprint)