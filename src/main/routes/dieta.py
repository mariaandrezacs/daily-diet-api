from flask import Blueprint, jsonify, request
from ..factories import calculator1_factory

dieta_rout_bp = Blueprint("dieta_routes", __name__)

@dieta_rout_bp.route("/dieta/criar", methods=["POST"])
def dieta():
    calc = calculator1_factory()
    response = calc.calculate(request)
    return jsonify(response)
