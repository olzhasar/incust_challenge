import os


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "incust")
    DEBUG = os.getenv("DEBUG", False)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://incust:incust@localhost/incust"
    )

    PAGINATION = 10


class TestConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
