# app/auth/utils.py
import bcrypt
import jwt
from datetime import datetime, timedelta

JWT_SECRET = "sweetshop_secret_key"
JWT_EXP_MIN = 60


def hash_password(raw: str) -> str:
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()


def check_password(raw: str, hashed: str) -> bool:
    return bcrypt.checkpw(raw.encode(), hashed.encode())


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=JWT_EXP_MIN)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
