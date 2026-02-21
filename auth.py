from flask import Blueprint, request, jsonify
import json
import os

auth_bp = Blueprint("auth", __name__)

USERS_FILE = "users.json"

# Create users.json if not exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)


def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    users = load_users()

    # check if user exists
    for user in users:
        if user["email"] == email:
            return jsonify({"message": "User already exists"}), 400

    users.append({
        "name": name,
        "email": email,
        "password": password
    })

    save_users(users)

    return jsonify({"message": "Registration successful"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    users = load_users()

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "message": "Login successful",
                "token": "demo-token"
            })

    return jsonify({"message": "Invalid credentials"}), 401
