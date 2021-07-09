from api.models import User, db
from api.schemas import UserChangeSchema, UserCreateSchema, UserSchema
from connexion import request
from flask import jsonify
from flask_jwt_extended import create_access_token, get_current_user, jwt_required
from pydantic import ValidationError
from sqlalchemy import exc


def login():
    try:
        validated = UserCreateSchema(**request.json)
    except ValidationError:
        return jsonify({"msg": "Invalid request"}), 400

    user = User.query.filter_by(username=validated.username).one_or_none()

    if not user or not user.check_password(validated.password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


def signup():
    try:
        validated = UserCreateSchema(**request.json)
    except ValidationError:
        return jsonify({"msg": "Invalid request"}), 400

    user = User(username=validated.username)
    user.set_password(validated.password)

    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Username is already taken"}), 400

    return UserSchema.from_orm(user).json(), 201


@jwt_required()
def update():
    user = get_current_user()

    try:
        validated = UserChangeSchema(**request.json)
    except ValidationError:
        return jsonify({"msg": "Invalid request"}), 400

    for key, value in validated.dict().items():
        setattr(user, key, value)

    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Username is already taken"}), 400

    return UserSchema.from_orm(user).json(), 200
