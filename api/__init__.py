import connexion
from flask_jwt_extended import JWTManager
from swagger_ui_bundle import swagger_ui_3_path

from api.config import Config, TestConfig
from api.models import User, db


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

    db.init_app(app.app)

    jwt = JWTManager(app.app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    return app
