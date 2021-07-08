import connexion
from swagger_ui_bundle import swagger_ui_3_path


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='./',
                             options={'swagger_path': swagger_ui_3_path})

    app.add_api('swagger.yaml')

    return app
