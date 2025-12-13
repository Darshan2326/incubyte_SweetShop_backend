from fastapi import FastAPI
# from app.auth.routes import router as auth_router
from app.user.routes import router as user_router
# from test.auth_TDD import router as auth_router // TDD test
app = FastAPI(title="Sweet Shop API")

app.include_router(user_router)
# app.include_router(auth_router) // TDD test
