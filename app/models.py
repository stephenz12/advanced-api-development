from app.extensions import db

# Association table for many-to-many (used later)
service_ticket_mechanics = db.Table(
    "service_ticket_mechanics",
    db.Column(
        "service_ticket_id",
        db.Integer,
        db.ForeignKey("service_ticket.id"),
        primary_key=True
    ),
    db.Column(
        "mechanic_id",
        db.Integer,
        db.ForeignKey("mechanic.id"),
        primary_key=True
    )
)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))

    service_tickets = db.relationship("ServiceTicket", backref="customer", lazy=True)


class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_mechanics,
        back_populates="mechanics"
    )


class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))

    mechanics = db.relationship(
        "Mechanic",
        secondary=service_ticket_mechanics,
        back_populates="service_tickets"
    )
