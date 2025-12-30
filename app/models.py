from app.extensions import db, bcrypt

# Association table (unchanged)
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
    ),
)

class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)  # 🔐 hashed password

    service_tickets = db.relationship(
        "ServiceTicket",
        backref="customer",
        lazy=True
    )

    # 🔐 SET password (hash it)
    def set_password(self, plain_password):
        self.password = bcrypt.generate_password_hash(
            plain_password
        ).decode("utf-8")

    # 🔐 CHECK password
    def check_password(self, plain_password):
        return bcrypt.check_password_hash(
            self.password,
            plain_password
        )


class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_mechanics,
        back_populates="mechanics"
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.id"),
        nullable=False
    )

    mechanics = db.relationship(
        "Mechanic",
        secondary=service_ticket_mechanics,
        back_populates="service_tickets"
    )
