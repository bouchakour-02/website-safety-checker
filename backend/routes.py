from flask import Blueprint, request, jsonify
from app import db
from models import User, ScanHistory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests
import re

main_bp = Blueprint("main_bp", __name__)

# Helper function: basic URL validation
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'\w+(?:[-\w]*\w+)*(?:\.\w+(?:[-\w]*\w+)*)+'  # domain...
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

@main_bp.route("/scan", methods=["POST"])
@jwt_required()
def scan_url():
    data = request.get_json()
    url = data.get("url")
    if not url or not is_valid_url(url):
        return jsonify({"msg": "Invalid URL provided"}), 400

    # --- SECURITY NOTE ---
    # Validate and sanitize URL input to avoid SSRF attacks.
    # In production, you might add further controls like whitelisting domains.

    # Example: Call an external API (e.g., VirusTotal) for URL safety check
    # (Replace 'YOUR_API_KEY' with a secure key from your environment)
    api_key = "YOUR_VIRUSTOTAL_API_KEY"
    vt_url = f"https://www.virustotal.com/api/v3/urls"
    
    # You might need to encode the URL or follow API documentation specifics.
    headers = {"x-apikey": api_key}
    # For demonstration, this is a placeholder call.
    try:
        response = requests.post(vt_url, headers=headers, data={"url": url})
        result = response.json()
    except Exception as e:
        result = {"error": "Failed to fetch data from external API", "details": str(e)}
    
    # Optionally, save scan results in the database for the logged in user
    user_id = get_jwt_identity()
    new_scan = ScanHistory(url=url, result=str(result), user_id=user_id)
    db.session.add(new_scan)
    db.session.commit()
    
    return jsonify(result), 200
