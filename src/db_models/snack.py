from ..repository.database import db


class Dieta(db.Model):
    """ - Nome, - Descrição, - Data e Hora, - Está dentro ou não da dieta """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    creat_at = db.Column(db.Datetime, nullable=True)
    in_dieta = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creat_at": self.creat_at,
            "in_dieta": self.in_dieta,
        }
