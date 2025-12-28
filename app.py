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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    products = db.relationship(
        'Product',
        secondary=order_product,
        backref=db.backref('orders', lazy=True)
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


# ----------------------
# SCHEMAS
# ----------------------
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

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
