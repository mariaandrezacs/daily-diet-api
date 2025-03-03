from flask import Flask
from main.routes.dieta import calc_rout_bp

app = Flask(__name__)

app.register_blueprint(calc_rout_bp)