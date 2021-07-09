import factory
from api.models import Product, ProductList, ProductPrice, User, db
from sqlalchemy.orm import scoped_session


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")

    class Meta:
        model = User
        sqlalchemy_session = db.session
