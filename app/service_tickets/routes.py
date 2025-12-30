from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import ticket_schema, tickets_schema


@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    data = request.get_json()

    ticket = ServiceTicket(
        description=data.get("description"),
        customer_id=data.get("customer_id")
    )

    db.session.add(ticket)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 201


@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 200
