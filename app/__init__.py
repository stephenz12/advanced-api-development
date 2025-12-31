from flask import Flask
from app.extensions import db, ma, limiter, cache, bcrypt, jwt

def create_app(config_class=None):
    app = Flask(__name__)

    # Secret keys
    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["JWT_SECRET_KEY"] = "jwt-super-secret-key"
    
    # Caching configuration
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 60

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)        # ✅ THIS WAS MISSING
    limiter.init_app(app)
    cache.init_app(app)

    # Register blueprints
    from app.customers import customers_bp
    from app.mechanics import mechanics_bp
    from app.service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
