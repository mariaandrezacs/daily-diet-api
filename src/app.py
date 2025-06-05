from datetime import datetime

from flask import Flask, jsonify, request
from flask_socketio import SocketIO

from db_models.refeicoes import Refeicoes
from repository.database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)
socketio = SocketIO(app)

# ENDPOINT: CREATE
@app.route("/created", methods=["POST"])
def create_diet():
    data = request.get_json()

    name = data.get("name")
    date_time_str = data.get("date_time")
    in_diet = data.get("in_diet")

    if not name or not date_time_str or in_diet is None:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    nova_refeicao = Refeicoes(
        name=name,
        description=data.get("description", ""),
        date_time=date_time,
        in_diet=in_diet
    )

    db.session.add(nova_refeicao)
    db.session.commit()

    return jsonify({'message': 'Meals created successfully'}), 201


# ENDPOINT: LIST
@app.route("/refeicoes", methods=["GET"])
def get_refeicoes():
    refeicoes = Refeicoes.query.all()
    data = [refeicao.to_dict() for refeicao in refeicoes]
    return jsonify({'refeicoes': data}), 200


# ENDPOINT: EDIT
@app.route('/refeicoes/update/<int:id>', methods=["PUT"])
def update_refeicao(id):
    refeicao = Refeicoes.query.get(id)

    if not refeicao:
        return jsonify({"message": "Não foi possível encontrar a refeição."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos ou ausentes."}), 400

    try:
        refeicao.name = data.get("name", refeicao.name)
        refeicao.description = data.get("description", refeicao.description)

        if "date_time" in data:
            try:
                refeicao.date_time = datetime.strptime(data["date_time"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return jsonify({"message": 
                                "Formato de data inválido. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

        refeicao.in_diet = data.get("in_diet", refeicao.in_diet)

        db.session.commit()
        return jsonify({"message": "Refeição atualizada com sucesso."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar refeição.", "error": str(e)}), 500


# ENDPOINT: DETAIL MEALS SPECIFIC
@app.route("/refeicoes/<int:id>", methods=["GET"])
def get_refeicoes_especifica(id):
    refeicoes = Refeicoes.query.all()
    for refeicao in refeicoes:
        if refeicao.id == id:
            return jsonify({'refeicoes': refeicao.to_dict()}), 200
    return jsonify({"message": "Refeição não encontrada."}), 404


# ENDPOINT: DELETE
@app.route("/refeicoes/<int:id>", methods=["DELETE"])
def delete_refeicao(id):
    delete_meal = None
    refeicoes = Refeicoes.query.all()
    for refeicao in refeicoes:
        if refeicao.id == id:
            delete_meal = refeicao
            break

    if delete_meal is None:
        return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404

    db.session.delete(delete_meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso."})



# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
