from datetime import datetime

from repository.database import db


class Refeicoes(db.Model):
    """ - Nome, - Descrição, - Data e Hora, - Está dentro ou não da dieta """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    in_diet = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_time": self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "in_diet": self.in_diet,
        }
    