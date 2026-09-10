import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_socketio import SocketIO
from werkzeug.security import check_password_hash, generate_password_hash

from db_models.refeicoes import Refeicoes
from db_models.usuarios import User
from repository.database import db
from seed import seed_database

app = Flask(__name__)
CORS(app, origins=["https://daily-diet-companion.vercel.app"])

database_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "SECRET_KEY_WEBSOCKET")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", app.config["SECRET_KEY"])

db.init_app(app)
jwt = JWTManager(app)
socketio = SocketIO(app)


@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


def get_current_user_id():
    return int(get_jwt_identity())


@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already taken"}), 409

    user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "id": user.id}), 201


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@app.route("/refeicoes", methods=["POST"])
@app.route("/created", methods=["POST"])
@jwt_required()
def create_diet():
    data = request.get_json()

    name = data.get("name")
    date_time_str = data.get("date_time")
    in_diet = data.get("in_diet")

    if not name or not date_time_str or in_diet is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400

    nova_refeicao = Refeicoes(
        name=name,
        description=data.get("description", ""),
        date_time=date_time,
        in_diet=in_diet,
        user_id=get_current_user_id()
    )

    db.session.add(nova_refeicao)
    db.session.commit()

    return jsonify({"message": "Meals created successfully"}), 201


@app.route("/refeicoes", methods=["GET"])
@jwt_required()
def get_refeicoes():
    refeicoes = Refeicoes.query.filter_by(user_id=get_current_user_id()).all()
    data = [refeicao.to_dict() for refeicao in refeicoes]
    return jsonify({"refeicoes": data}), 200


@app.route("/refeicoes/<int:id>", methods=["PUT"])
@app.route("/refeicoes/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_refeicao(id):
    user_id = get_current_user_id()
    refeicao = Refeicoes.query.filter_by(id=id, user_id=user_id).first()

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
                return jsonify({"message": "Formato de data inválido. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

        refeicao.in_diet = data.get("in_diet", refeicao.in_diet)

        db.session.commit()
        return jsonify({"message": "Refeição atualizada com sucesso."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar refeição.", "error": str(e)}), 500


@app.route("/refeicoes/<int:id>", methods=["GET"])
@jwt_required()
def get_refeicoes_especifica(id):
    user_id = get_current_user_id()
    refeicao = Refeicoes.query.filter_by(id=id, user_id=user_id).first()

    if not refeicao:
        return jsonify({"message": "Refeição não encontrada."}), 404

    return jsonify({"refeicoes": refeicao.to_dict()}), 200


@app.route("/refeicoes/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_refeicao(id):
    user_id = get_current_user_id()
    refeicao = Refeicoes.query.filter_by(id=id, user_id=user_id).first()

    if not refeicao:
        return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404

    db.session.delete(refeicao)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso."})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5008)),
        allow_unsafe_werkzeug=True
    )
