from backend.app.models.user_model import fake_users_db
from app.security.hash import hash_password, verify_password
from app.security.jwt_handler import create_access_token

def register_user(email: str, password: str):
    if email in fake_users_db:
        return None

    hashed = hash_password(password)

    fake_users_db[email] = {
        "email": email,
        "password": hashed
    }

    return fake_users_db[email]

def login_user(email: str, password: str):
    user = fake_users_db.get(email)

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    token = create_access_token({"sub": email})

    return token