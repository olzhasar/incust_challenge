from typing import List

from api.models import Product, ProductList, ProductPrice, db
from api.schemas import PriceSchema
from connexion import request
from flask import abort
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError, parse_obj_as
from sqlalchemy import exc


@jwt_required()
def create(product_id: int):
    try:
        validated = parse_obj_as(List[PriceSchema], request.json)
    except ValidationError as e:
        abort(400, str(e))

    user = get_current_user()

    product = (
        Product.query.with_entities(Product.id)
        .join(ProductList)
        .filter(Product.id == product_id, ProductList.user_id == user.id)
        .first()
    )
    if product is None:
        abort(400, "Invalid product_id")

    for row in validated:
        price = ProductPrice(product_id=product_id, **row.dict())
        db.session.add(price)

        try:
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400, "Only one price can be specified for each currency code")

    db.session.commit()

    return [v.dict() for v in validated], 201


@jwt_required()
def delete(product_id: int, currency_code: str):
    user = get_current_user()

    price = (
        ProductPrice.query.join(Product)
        .join(ProductList)
        .filter(
            ProductPrice.product_id == product_id,
            ProductPrice.currency_code == currency_code,
            ProductList.user_id == user.id,
        )
        .first_or_404()
    )

    db.session.delete(price)
    db.session.commit()

    return "", 204
