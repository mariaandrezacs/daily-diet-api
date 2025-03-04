from datetime import datetime

from flask import Flask, request
from flask_socketio import SocketIO

from db_models.refeicoes import Refeicoes
from repository.database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)
socketio = SocketIO(app)


@app.route('/created', methods=['POST'])
def create_diet():
    data = request.get_json()
    nova_refeicao = Refeicoes(
        name=data["name"],
        description=data.get("description", ""),
        date_time=datetime.strptime(data["date_time"], "%Y-%m-%d %H:%M:%S"),
        in_diet=data["in_diet"],
    )
    db.session.add(nova_refeicao)
    db.session.commit()
    return {'message': 'Meals created successfully'}, 201





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
