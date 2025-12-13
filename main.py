from fastapi import FastAPI
# from app.auth.routes import router as auth_router
from app.user.routes import router as user_router
app = FastAPI(title="Sweet Shop API")

app.include_router(user_router)
