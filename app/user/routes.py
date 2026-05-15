from fastapi import APIRouter, HTTPException
from app.user.models import LoginForm

router = APIRouter(prefix="", tags=["auth"])

STATIC_USERS = {
    "admin@demo.com": {
        "id": "demo-admin-id",
        "name": "Admin User",
        "email": "admin@demo.com",
        "password": "admin123",
        "role": "admin"
    },
    "user@demo.com": {
        "id": "demo-user-id",
        "name": "Demo User",
        "email": "user@demo.com",
        "password": "user123",
        "role": "user"
    }
}

@router.post("/api/auth/login")
async def UserLogin(form: LoginForm):
    user = STATIC_USERS.get(form.email)
    if not user or user["password"] != form.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "token": "demo-token",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }
