from flask import request, jsonify
from app.extensions import db
from app.models import Mechanic
from app.mechanics import mechanics_bp
from app.mechanics.schemas import mechanic_schema, mechanics_schema


@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    data = request.get_json()

    mechanic = Mechanic(
        name=data.get("name"),
        specialty=data.get("specialty")
    )

    db.session.add(mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 201


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()

    mechanic.name = data.get("name", mechanic.name)
    mechanic.specialty = data.get("specialty", mechanic.specialty)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic deleted"}), 200
