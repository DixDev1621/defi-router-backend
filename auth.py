from flask import Blueprint, request, jsonify
import json
import os
import bcrypt
import uuid

auth_bp = Blueprint("auth", __name__)

USERS_FILE = "users.json"

# ------------------------
# Utility Functions
# ------------------------

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ------------------------
# REGISTER
# ------------------------

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields required"}), 400

    users = load_users()

    # Check if email already exists
    for user in users:
        if user["email"] == email:
            return jsonify({"message": "Email already exists"}), 400

    # 🔐 Hash password
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": hashed_pw.decode("utf-8")
    }

    users.append(new_user)
    save_users(users)

    return jsonify({"message": "User registered successfully"}), 201

# ------------------------
# LOGIN
# ------------------------

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    users = load_users()

    for user in users:
        if user["email"] == email:
            # 🔐 Compare hashed password
            if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                token = str(uuid.uuid4())
                return jsonify({"message": "Login successful", "token": token}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "User not found"}), 404