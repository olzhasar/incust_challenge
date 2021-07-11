from api.models import Product, ProductList, db
from api.schemas import ProductCreateSchema, ProductSchema
from connexion import request
from flask import abort
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError
from sqlalchemy import exc
from werkzeug.utils import secure_filename


@jwt_required()
def create():
    try:
        validated = ProductCreateSchema(**request.form)
    except ValidationError as e:
        abort(400, str(e))

    user = get_current_user()
    data = validated.dict()

    product_list = (
        ProductList.query.with_entities(ProductList.id)
        .filter_by(id=data["product_list_id"], user_id=user.id)
        .first()
    )

    if not product_list:
        abort(400, "Invalid product list id")

    product = Product(**data)

    image = request.files.get("image")
    if image:
        filename = secure_filename(image.filename)
        product.image = filename
        image.save(product.image_filepath)

    db.session.add(product)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        abort(400, "Each product must have a unique SKU inside product list")

    return ProductSchema.from_orm(product).dict(), 201


@jwt_required()
def delete(product_id: int):
    user = get_current_user()
    product = (
        Product.query.join(ProductList)
        .filter(Product.id == product_id, ProductList.user_id == user.id)
        .first_or_404()
    )

    db.session.delete(product)
    db.session.commit()

    return "", 204
