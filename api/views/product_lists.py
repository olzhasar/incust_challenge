from api.models import Product, ProductList, ProductPrice, db
from api.schemas import ProductListCreateSchema, ProductListSchema
from connexion import request
from flask import abort
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError
from sqlalchemy import exc


@jwt_required()
def create():
    try:
        validated = ProductListCreateSchema(**request.json)
    except ValidationError as e:
        return e.json(), 400

    user = get_current_user()

    data = validated.dict()
    products_data = data.pop("products")

    product_list = ProductList(user_id=user.id, **data)

    db.session.add(product_list)
    db.session.flush()

    for product_row in products_data:
        prices_data = product_row.pop("prices")

        product = Product(product_list_id=product_list.id, **product_row)

        db.session.add(product)
        try:
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400, "Each product must have a unique SKU inside product list")

        for price_row in prices_data:
            db.session.add(ProductPrice(product_id=product.id, **price_row))

            try:
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
                abort(400, "Only one price value is allowed for each currency code")

    db.session.commit()

    return ProductListSchema.from_orm(product_list).json(), 201


@jwt_required()
def read_one():
    pass


@jwt_required()
def read_all():
    pass


@jwt_required()
def delete():
    pass
