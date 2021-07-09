from api.models import User, db
from api.schemas import UserChangeSchema, UserCreateSchema, UserSchema
from connexion import request
from flask import abort, jsonify
from flask_jwt_extended import create_access_token, get_current_user, jwt_required
from pydantic import ValidationError
from sqlalchemy import exc


def login():
    try:
        validated = UserCreateSchema(**request.json)
    except ValidationError as e:
        abort(400, str(e))

    user = User.query.filter_by(username=validated.username).one_or_none()

    if not user or not user.check_password(validated.password):
        abort(401, "Invalid credentials")

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


def signup():
    try:
        validated = UserCreateSchema(**request.json)
    except ValidationError as e:
        abort(400, str(e))

    data = validated.dict()
    password = data.pop("password")

    user = User(**data)
    user.set_password(password)

    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        abort(400, "Username is already taken")

    return UserSchema.from_orm(user).json(), 201


@jwt_required()
def update():
    user = get_current_user()

    try:
        validated = UserChangeSchema(**request.json)
    except ValidationError as e:
        abort(400, str(e))

    for key, value in validated.dict().items():
        setattr(user, key, value)

    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        abort(400, "Username is already taken")

    return UserChangeSchema.from_orm(user).json(), 200
