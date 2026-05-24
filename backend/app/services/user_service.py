from datetime import datetime

import app.core.database as database
from app.core.security import (
    hash_password,
    verify_password
)
from pymongo.errors import PyMongoError


db = database.get_database()
collection = db.users
memory_users = {}


def register_user(
    email: str,
    password: str
):
    if not email or not password:
        return {
            "success": False,
            "message": "Email and password are required"
        }

    try:
        existing = collection.find_one({"email": email})
        if existing:
            return {
                "success": False,
                "message": "User already exists"
            }

        collection.insert_one({
            "email": email,
            "password": hash_password(password),
            "created_at": datetime.utcnow()
        })

        return {
            "success": True
        }
    except PyMongoError:
        if email in memory_users:
            return {
                "success": False,
                "message": "User already exists"
            }

        memory_users[email] = {
            "email": email,
            "password": hash_password(password),
            "created_at": datetime.utcnow()
        }

        return {
            "success": True
        }


def authenticate_user(
    email: str,
    password: str
):
    try:
        user = collection.find_one({"email": email})
    except PyMongoError:
        user = memory_users.get(email)

    if not user:
        return None

    if not verify_password(
        password,
        user["password"]
    ):
        return None

    return {
        "email": user["email"]
    }
