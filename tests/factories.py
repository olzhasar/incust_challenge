import factory
from api.models import Product, ProductList, ProductPrice, User, db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")

    class Meta:
        model = User
        sqlalchemy_session = db.session


class ProductListFactory(factory.alchemy.SQLAlchemyModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("word")

    class Meta:
        model = ProductList
        sqlalchemy_session = db.session


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    sku = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    product_list = factory.SubFactory(ProductListFactory)

    class Meta:
        model = Product
        sqlalchemy_session = db.session


class ProductPriceFactory(factory.alchemy.SQLAlchemyModelFactory):
    product = factory.SubFactory(ProductFactory)
    value = factory.Faker("pydecimal", left_digits=6, right_digits=2)
    currency_code = factory.Faker("currency_code")

    class Meta:
        model = ProductPrice
        sqlalchemy_session = db.session
