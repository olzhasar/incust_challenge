import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    avatar_url = db.Column(db.String, nullable=True)

    def set_password(self, raw_password: str):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode(), salt).decode("utf-8")

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())


class ProductList(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("product_lists", lazy=True))


class Product(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    sku = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    product_list_id = db.Column(
        db.Integer, db.ForeignKey("product_list.id"), nullable=False
    )
    product_list = db.relationship(
        "ProductList", backref=db.backref("products", lazy=True)
    )

    __table_args__ = (db.UniqueConstraint("sku", "product_list_id"),)


class ProductPrice(db.Model):
    value = db.Column(db.Numeric(10, 2), nullable=False)
    currency_code = db.Column(db.String(4), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product", backref=db.backref("prices", lazy=True))

    __table_args__ = (db.PrimaryKeyConstraint("value", "currency_code"),)
