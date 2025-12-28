from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

# ----------------------
# DATABASE CONFIG
# ----------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12Supername5!@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# ----------------------
# MODELS
# ----------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    products = db.relationship(
        "Product",
        secondary=order_product,
        back_populates="orders"
    )


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship(
        "Order",
        secondary=order_product,
        back_populates="products"
    )

# ----------------------
# SCHEMAS
# ----------------------

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product


class OrderSchema(ma.SQLAlchemyAutoSchema):
    products = ma.Nested(ProductSchema, many=True)

    class Meta:
        model = Order
        include_fk = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# ----------------------
# ROUTES
# ----------------------
@app.route("/")
def home():
    return "FLASK IS RUNNING"

@app.route("/ping")
def ping():
    return {"status": "ok"}

# -------- USERS --------
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return {"error": "name and email required"}, 400

    user = User(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), 201


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.dump(users)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted successfully"}, 200

# -------- ORDERS --------
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data or "user_id" not in data:
        return {"error": "user_id required"}, 400

    user = User.query.get(data["user_id"])
    if not user:
        return {"error": "User does not exist"}, 400

    order = Order(user_id=user.id)

    db.session.add(order)
    db.session.commit()

    return order_schema.dump(order), 201


@app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return orders_schema.dump(orders)


@app.route("/orders/<int:order_id>/add_product/<int:product_id>", methods=["PUT"])
def add_product_to_order(order_id, product_id):
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    if not order or not product:
        return {"error": "Order or Product not found"}, 404

    if product in order.products:
        return {"error": "Product already in order"}, 400

    order.products.append(product)
    db.session.commit()

    return order_schema.dump(order), 200

    # -------- PRODUCTS --------
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data or "product_name" not in data or "price" not in data:
        return {"error": "product_name and price required"}, 400

    product = Product(
        product_name=data["product_name"],
        price=data["price"]
    )

    db.session.add(product)
    db.session.commit()

    return product_schema.dump(product), 201


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.dump(products)


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return {"error": "Product not found"}, 404

    db.session.delete(product)
    db.session.commit()

    return {"message": "Product deleted successfully"}, 200


# ----------------------
# CREATE TABLES
# ----------------------
with app.app_context():
    db.create_all()

# ----------------------
# RUN APP
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
