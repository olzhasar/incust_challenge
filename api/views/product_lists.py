from api.models import Product, ProductList, db
from api.schemas import (
    ProductListCreateSchema,
    ProductListSchema,
    ProductListShortSchema,
)
from connexion import request
from flask import abort, current_app, jsonify
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError


@jwt_required()
def create():
    try:
        validated = ProductListCreateSchema(**request.json)
    except ValidationError as e:
        abort(400, str(e))

    user = get_current_user()

    data = validated.dict()

    product_list = ProductList(user_id=user.id, **data)

    db.session.add(product_list)
    db.session.commit()

    return ProductListSchema.from_orm(product_list).json(), 201


@jwt_required()
def read_all():
    user = get_current_user()

    product_lists = ProductList.query.filter_by(user_id=user.id)

    data = [ProductListShortSchema.from_orm(p).dict() for p in product_lists]
    return jsonify({"results": data}), 200


@jwt_required()
def read_one(
    list_id: int,
    sort_by: str = None,
    product_sku: str = None,
    product_name: str = None,
    page: int = None,
):
    user = get_current_user()

    product_list = ProductList.query.filter_by(
        id=list_id, user_id=user.id
    ).first_or_404()

    query = Product.query.filter_by(product_list_id=product_list.id)

    if product_name:
        query = query.filter(Product.name.like(f"%{product_name}%"))

    if product_sku:
        query = query.filter_by(sku=product_sku)

    if sort_by == "sku":
        query = query.order_by(Product.sku)
    elif sort_by == "name":
        query = query.order_by(Product.name)

    per_page = current_app.config["PAGINATION"]
    products = query.paginate(page=page, per_page=per_page).items

    schema = ProductListSchema(
        id=product_list.id,
        name=product_list.name,
        products=products,
    )

    return schema.dict(), 200


@jwt_required()
def delete(list_id: int):
    user = get_current_user()
    product_list = ProductList.query.filter_by(
        id=list_id, user_id=user.id
    ).first_or_404()

    db.session.delete(product_list)
    db.session.commit()

    return "", 204
