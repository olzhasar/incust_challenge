import connexion
from flask_jwt_extended import JWTManager
from swagger_ui_bundle import swagger_ui_3_path

from api.config import Config, TestConfig
from api.models import db


def create_app(testing=False):
    app = connexion.FlaskApp(
        __name__,
        specification_dir="./",
        options={
            "swagger_path": swagger_ui_3_path,
        },
    )

    app.add_api("swagger.yaml")

    config = Config if not testing else TestConfig
    app.app.config.from_object(config)

    JWTManager(app.app)

    db.init_app(app.app)

    return app
