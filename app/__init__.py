from flask import Flask
from app.extensions import db, ma

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    from app.customers import customers_bp
    from app.mechanics import mechanics_bp
    from app.service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")

    with app.app_context():
        db.create_all()

    return app
