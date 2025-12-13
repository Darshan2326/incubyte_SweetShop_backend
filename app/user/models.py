# app/auth/models.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Pydantic models for incoming requests
class RegisterForm(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginForm(BaseModel):
    email: EmailStr
    password: str


# Simple representation of stored user data
class UserInDB(BaseModel):
    id: str
    name: str
    email: EmailStr
    password_hash: str
    created_at: datetime
