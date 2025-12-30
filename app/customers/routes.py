from flask import request, jsonify
from app.extensions import db
from app.models import Customer
from app.customers import customers_bp
from app.customers.schemas import customer_schema, customers_schema
@customers_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()

    customer = Customer(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone")
    )

    db.session.add(customer)
    db.session.commit()

    return customer_schema.jsonify(customer), 201
@customers_bp.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers), 200
@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone = data.get("phone", customer.phone)

    db.session.commit()
    return customer_schema.jsonify(customer), 200
@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200
