from connexion import request
from flask import jsonify
from flask_jwt_extended import create_access_token

from api.models import User


def login():
    try:
        username = request.json["username"]
        password = request.json["password"]
    except KeyError:
        return jsonify({"msg": "Invalid request"}), 400

    user = User.query.filter_by(name=username).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


def signup():
    pass
