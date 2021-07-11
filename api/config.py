import os


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "incust")
    DEBUG = os.getenv("DEBUG", False)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://incust:incust@localhost/incust"
    )

    PAGINATION = 10

    BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
    MEDIA_DIR = os.path.join(BASE_DIR, "media/")


class TestConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
