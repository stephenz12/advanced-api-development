from flask import request, jsonify
from app.extensions import db, bcrypt
from app.models import Customer
from app.customers import customers_bp
from app.customers.schemas import (
    customer_schema,
    customers_schema,
    login_schema
)
from app.utils.auth import encode_token, token_required


# =========================
# REGISTER CUSTOMER
# =========================
@customers_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()

    if Customer.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    customer = Customer(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        password=hashed_password
    )

    db.session.add(customer)
    db.session.commit()

    return customer_schema.jsonify(customer), 201


# =========================
# LOGIN CUSTOMER
# =========================
@customers_bp.route("/login", methods=["POST"])
def login_customer():
    data = request.get_json()

    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    customer = Customer.query.filter_by(email=data["email"]).first()
    if not customer:
        return jsonify({"error": "Invalid email or password"}), 401

    if not bcrypt.check_password_hash(customer.password, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(customer.id)

    return jsonify({
        "token": token,
        "customer_id": customer.id
    }), 200


# =========================
# GET ALL CUSTOMERS (PROTECTED)
# =========================
@customers_bp.route("/", methods=["GET"])
@token_required
def get_customers(customer_id):
    customers = Customer.query.all()
    return customers_schema.jsonify(customers), 200


# =========================
# UPDATE CUSTOMER (OWNER ONLY)
# =========================
@customers_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "Unauthorized"}), 403

    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.phone = data.get("phone", customer.phone)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# =========================
# DELETE CUSTOMER (OWNER ONLY)
# =========================
@customers_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"error": "Unauthorized"}), 403

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200
