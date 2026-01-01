from flask import jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from app import create_app

app = create_app()

# -------------------------
# Swagger Configuration
# -------------------------
SWAGGER_URL = "/swagger"
API_URL = "/swagger.json"

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "E-Commerce API"}
)

app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

@app.route("/swagger.json")
def swagger_json():
    swag = swagger(app)

    swag["info"] = {
        "title": "E-Commerce API",
        "version": "1.0"
    }

    swag["host"] = "advanced-api-development.onrender.com"
    swag["schemes"] = ["https"]

    swag["securityDefinitions"] = {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme"
        }
    }

    return jsonify(swag)