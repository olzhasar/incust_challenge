import os

from api.models import User, db
from api.schemas import UserCreateSchema, UserSchema
from connexion import request
from flask import abort, jsonify
from flask_jwt_extended import create_access_token, get_current_user, jwt_required
from pydantic import ValidationError
from sqlalchemy import exc
from werkzeug.utils import secure_filename


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
        validated = UserCreateSchema(**request.form)
    except ValidationError as e:
        abort(400, str(e))

    data = validated.dict()
    password = data.pop("password")

    user = User(**data)
    user.set_password(password)

    avatar = request.files.get("avatar")
    if avatar:
        filename = secure_filename(avatar.filename)
        user.avatar = filename
        avatar.save(user.avatar_filepath)

    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        abort(400, "Username is already taken")

    return UserSchema.from_orm(user).dict(), 201


@jwt_required()
def update():
    user = get_current_user()

    new_username = request.form.get("username")
    if new_username:
        user.username = new_username

    avatar = request.files.get("avatar")
    if avatar:
        if user.avatar:
            os.remove(user.avatar_filepath)

        filename = secure_filename(avatar.filename)
        user.avatar = filename
        avatar.save(user.avatar_filepath)

    db.session.add(user)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        abort(400, "Username is already taken")

    return UserSchema.from_orm(user).dict(), 200
