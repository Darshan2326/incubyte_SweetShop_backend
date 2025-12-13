# app/auth/routes.py
from fastapi import APIRouter
from app.user.utils import hash_password,check_password, create_token
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

    data = {
        "_id": user_id,
        "name": form.name,
        "email": form.email,
        "password_hash": hashed,
        "created_at": datetime.utcnow()
    }

    await users_collection.insert_one(data)

    token = create_token({"id": user_id, "email": form.email})

    return {
        "message": "User registered successfully",
        "token": token,
        "user": {
            "id": user_id,
            "name": form.name,
            "email": form.email,
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

    token = create_token(
        {"id": find_in_user_collection["_id"], "email": find_in_user_collection["email"]})

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": find_in_user_collection["_id"],
            "name": find_in_user_collection["name"],
            "email": find_in_user_collection["email"],
        }
    }


