from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from app.extensions import db, bcrypt
from app.models import Customer
from app.customers import customers_bp
from app.customers.schemas import (
    customer_schema,
    customers_schema,
    login_schema
)

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

    # ✅ FIX: identity MUST be a string
    token = create_access_token(identity=str(customer.id))

    return jsonify({
        "access_token": token,
        "customer_id": customer.id
    }), 200


# =========================
# GET ALL CUSTOMERS (PROTECTED)
# =========================
@customers_bp.route("/", methods=["GET"])
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers), 200


# =========================
# UPDATE CUSTOMER (OWNER ONLY)
# =========================
@customers_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_customer(id):
    # ✅ FIX: cast identity back to int
    customer_id = int(get_jwt_identity())

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
@jwt_required()
def delete_customer(id):
    # ✅ FIX: cast identity back to int
    customer_id = int(get_jwt_identity())

    if customer_id != id:
        return jsonify({"error": "Unauthorized"}), 403

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200
