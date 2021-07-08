import connexion
from flask_jwt_extended import JWTManager
from swagger_ui_bundle import swagger_ui_3_path

from api.models import db


def create_app():
    app = connexion.FlaskApp(
        __name__,
        specification_dir="./",
        options={
            "swagger_path": swagger_ui_3_path,
        },
    )

    app.add_api("swagger.yaml")

    app.app.config["JWT_SECRET_KEY"] = "secret"
    JWTManager(app.app)

    db.init_app(app.app)

    return app
