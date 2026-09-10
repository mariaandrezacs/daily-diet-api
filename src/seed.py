import json
import os
from datetime import datetime

from werkzeug.security import generate_password_hash

from db_models.refeicoes import Refeicoes
from db_models.usuarios import User
from repository.database import db


def seed_database():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixture.json")
    if not os.path.exists(fixture_path):
        return

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if User.query.first() is None:
        for user_data in data.get("users", []):
            db.session.add(User(
                username=user_data["username"],
                password_hash=generate_password_hash(user_data.get("password", "123456"))
            ))
        db.session.commit()

    admin = User.query.first()
    if admin and Refeicoes.query.first() is None:
        for ref in data.get("refeicoes", []):
            date_time = datetime.strptime(ref["date_time"], "%Y-%m-%d %H:%M:%S")
            db.session.add(Refeicoes(
                name=ref["name"],
                description=ref.get("description", ""),
                date_time=date_time,
                in_diet=ref["in_diet"],
                user_id=admin.id
            ))
        db.session.commit()
