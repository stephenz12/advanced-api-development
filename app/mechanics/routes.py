from flask import request, jsonify
from app.extensions import db, limiter, cache
from app.models import Mechanic
from app.mechanics import mechanics_bp
from app.mechanics.schemas import mechanic_schema, mechanics_schema


# =========================
# CREATE MECHANIC
# =========================
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    """
    Create mechanic
    ---
    tags:
      - Mechanics
    summary: Create a new mechanic
    parameters:
      - in: body
        name: body
        schema:
          properties:
            name:
              type: string
            specialty:
              type: string
    responses:
      201:
        description: Mechanic created
    """
    data = request.get_json()

    mechanic = Mechanic(
        name=data.get("name"),
        specialty=data.get("specialty")
    )

    db.session.add(mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 201


# =========================
# GET ALL MECHANICS
# =========================
@cache.cached(timeout=60)
@limiter.limit("5 per minute")
@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    """
    Get all mechanics
    ---
    tags:
      - Mechanics
    summary: Retrieve all mechanics
    description: Returns a list of all mechanics (cached and rate-limited)
    responses:
      200:
        description: List of mechanics
    """
    mechanics = Mechanic.query.all()
    return mechanics_schema.jsonify(mechanics), 200


# =========================
# UPDATE MECHANIC
# =========================
@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    """
    Update mechanic
    ---
    tags:
      - Mechanics
    summary: Update mechanic information
    parameters:
      - in: path
        name: id
        type: integer
      - in: body
        name: body
        schema:
          properties:
            name:
              type: string
            specialty:
              type: string
    responses:
      200:
        description: Mechanic updated
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()

    mechanic.name = data.get("name", mechanic.name)
    mechanic.specialty = data.get("specialty", mechanic.specialty)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# =========================
# DELETE MECHANIC
# =========================
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    """
    Delete mechanic
    ---
    tags:
      - Mechanics
    summary: Delete mechanic
    parameters:
      - in: path
        name: id
        type: integer
    responses:
      200:
        description: Mechanic deleted
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic deleted"}), 200
