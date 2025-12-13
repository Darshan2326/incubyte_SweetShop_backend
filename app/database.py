# # app/database.py
# import uuid
# from datetime import datetime
# from app.auth.models import UserInDB

# # using in-memory dict for sample logic, replace this with real DB
# db_users = {}


# def create_user(name, email, password_hash):
#     user_id = str(uuid.uuid4())
#     user = UserInDB(
#         id=user_id,
#         name=name,
#         email=email,
#         password_hash=password_hash,
#         created_at=datetime.utcnow()
#     )
#     db_users[email] = user
#     return user


# def find_user_by_email(email: str):
#     return db_users.get(email)


# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://Incubyte_db:Incubyte_db_pass@incubyte.vee5h8v.mongodb.net/?appName=Incubyte"

client = AsyncIOMotorClient(MONGO_URL)
db = client["sweetshop"]

users_collection = db["users"]
