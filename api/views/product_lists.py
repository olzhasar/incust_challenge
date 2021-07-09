from api.models import Product, ProductList, ProductPrice, db
from api.schemas import (
    ProductListCreateSchema,
    ProductListSchema,
    ProductListShortSchema,
)
from connexion import request
from flask import abort, jsonify
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError
from sqlalchemy import exc


@jwt_required()
def create():
    try:
        validated = ProductListCreateSchema(**request.json)
    except ValidationError as e:
        abort(400, str(e))

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
def read_all():
    user = get_current_user()

    product_lists = ProductList.query.filter_by(user_id=user.id)

    data = [ProductListShortSchema.from_orm(p).dict() for p in product_lists]
    return jsonify({"product_lists": data}), 200


@jwt_required()
def read_one(list_id: int):
    user = get_current_user()
    product_list = ProductList.query.get_or_404(list_id)

    if product_list.user_id != user.id:
        abort(401)

    return ProductListSchema.from_orm(product_list).dict(), 200


@jwt_required()
def delete(list_id: int):
    user = get_current_user()
    product_list = ProductList.query.get_or_404(list_id)

    if product_list.user_id != user.id:
        abort(401)

    db.session.delete(product_list)
    db.session.commit()

    return "", 204
