from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import ticket_schema, tickets_schema


# =========================
# CREATE SERVICE TICKET
# =========================
@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    """
    Create service ticket
    ---
    tags:
      - Service Tickets
    summary: Create a new service ticket
    parameters:
      - in: body
        name: body
        schema:
          properties:
            description:
              type: string
            customer_id:
              type: integer
    responses:
      201:
        description: Service ticket created
    """
    data = request.get_json()

    ticket = ServiceTicket(
        description=data.get("description"),
        customer_id=data.get("customer_id")
    )

    db.session.add(ticket)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 201


# =========================
# GET ALL SERVICE TICKETS
# =========================
@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    """
    Get all service tickets
    ---
    tags:
      - Service Tickets
    summary: Retrieve all service tickets
    responses:
      200:
        description: List of service tickets
    """
    tickets = ServiceTicket.query.all()
    return tickets_schema.jsonify(tickets), 200


# =========================
# ASSIGN MECHANIC TO TICKET
# =========================
@service_tickets_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>",
    methods=["PUT"]
)
def assign_mechanic(ticket_id, mechanic_id):
    """
    Assign mechanic to service ticket
    ---
    tags:
      - Service Tickets
    summary: Assign a mechanic to a service ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
      - in: path
        name: mechanic_id
        type: integer
    responses:
      200:
        description: Mechanic assigned to ticket
      404:
        description: Ticket or mechanic not found
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 200


# =========================
# REMOVE MECHANIC FROM TICKET
# =========================
@service_tickets_bp.route(
    "/<int:ticket_id>/remove-mechanic/<int:mechanic_id>",
    methods=["PUT"]
)
def remove_mechanic(ticket_id, mechanic_id):
    """
    Remove mechanic from service ticket
    ---
    tags:
      - Service Tickets
    summary: Remove a mechanic from a service ticket
    parameters:
      - in: path
        name: ticket_id
        type: integer
      - in: path
        name: mechanic_id
        type: integer
    responses:
      200:
        description: Mechanic removed from ticket
      404:
        description: Ticket or mechanic not found
    """
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return ticket_schema.jsonify(ticket), 200
