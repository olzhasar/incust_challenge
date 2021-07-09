import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def set_password(self, raw_password: str):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode(), salt).decode("utf-8")

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())
