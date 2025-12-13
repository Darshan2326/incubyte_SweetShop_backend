# app/auth/routes.py
from fastapi import APIRouter, HTTPException
from app.user.models import RegisterForm, LoginForm
from app.user.utils import hash_password, check_password, create_token
from app.database import users_collection
from datetime import datetime
import uuid

router = APIRouter(prefix="", tags=["auth"])


@router.post("/api/auth/register")
async def UserRegister(form: RegisterForm):
    user_in_db = await users_collection.find_one({"email": form.email})
    if user_in_db:
        raise HTTPException(
            status_code=400, detail="Entered email is already register please try to login")

    user_id = str(uuid.uuid4())

    hashed = hash_password(form.password)

    # Check if this should be an admin user (you can modify this condition as needed)
    # For example, you could check if the email is in a predefined list of admin emails
    role = "admin" if "@admin." in form.email or form.email.endswith(
        "@sweetshop.com") else "user"

    data = {
        "_id": user_id,
        "name": form.name,
        "email": form.email,
        "password_hash": hashed,
        "role": role,  # Adding role to user data
        "created_at": datetime.utcnow()
    }

    await users_collection.insert_one(data)

    token = create_token({"id": user_id, "email": form.email, "role": role})

    return {
        "message": "User registered successfully",
        "token": token,
        "user": {
            "id": user_id,
            "name": form.name,
            "email": form.email,
            "role": role
        }
    }


@router.post("/api/auth/login")
async def UserLogin(form: LoginForm):
    find_in_user_collection = await users_collection.find_one({"email": form.email})
    if not find_in_user_collection:
        raise HTTPException(
            status_code=401, detail="Invalid credentials plesae check the username and password")

    if not check_password(form.password, find_in_user_collection["password_hash"]):
        raise HTTPException(
            status_code=401, detail="Invalid credentials plesae check the username and password")

    # Include role in the token
    token = create_token(
        {
            "id": find_in_user_collection["_id"],
            "email": find_in_user_collection["email"],
            "role": find_in_user_collection.get("role", "user")
        })

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": find_in_user_collection["_id"],
            "name": find_in_user_collection["name"],
            "email": find_in_user_collection["email"],
            "role": find_in_user_collection.get("role", "user")
        }
    }
