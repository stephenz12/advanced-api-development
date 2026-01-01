from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from app.extensions import db, ma, limiter, cache, bcrypt, jwt

def create_app(config_class=None):
    app = Flask(__name__)

    # Default config
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["JWT_SECRET_KEY"] = "jwt-dev-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config_class:
        app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # ✅ IMPORT MODELS (CORRECT LOCATION)
    from app.models import Customer, Mechanic, ServiceTicket

    # ✅ CREATE TABLES
    with app.app_context():
        db.create_all()

    # ✅ REGISTER BLUEPRINTS
    from app.auth import auth_bp
    from app.customers import customers_bp
    from app.mechanics import mechanics_bp
    from app.service_tickets import service_tickets_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")

            
    return app
