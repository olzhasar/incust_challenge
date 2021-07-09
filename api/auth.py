from connexion import request
from flask import jsonify
from flask_jwt_extended import create_access_token
from pydantic import ValidationError

from api.models import User, UserSchema


def login():
    try:
        validated = UserSchema(**request.json)
    except ValidationError:
        return jsonify({"msg": "Invalid request"}), 400

    user = User.query.filter_by(username=validated.username).first()

    if not user or not user.check_password(validated.password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=validated.username)
    return jsonify(access_token=access_token)


def signup():
    pass
