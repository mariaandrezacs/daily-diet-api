from flask import Flask, jsonify, render_template, request, send_file
from repository.database import db
from db_models.snack import Dieta
from datetime import datetime, timedelta
from diet.diet import Diet
from flask_socketio import SocketIO


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)
socketio = SocketIO(app)


@app.route('/created', methods=['POST'])
def create_diet():
    data = request.get_json()
    print(data)
    return jsonify({"message": "Dados inválidos."}), 400





if __name__ == "__main__":
    app.run(debug=True)

    
    
