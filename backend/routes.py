from flask import Blueprint, request, jsonify
from app import db
from models import User, ScanHistory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests
import re

main_bp = Blueprint("main_bp", __name__)

def is_valid_url(url):
    # Basic URL validation using regex
    regex = re.compile(
        r'^(?:http|ftp)s?://'  
        r'\w+(?:[-\w]*\w+)*(?:\.\w+(?:[-\w]*\w+)*)+'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@main_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@main_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401
