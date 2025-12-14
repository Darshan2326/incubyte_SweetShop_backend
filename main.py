from fastapi import FastAPI
# from app.auth.routes import router as auth_router
from app.user.routes import router as user_router
# from test.auth_TDD import router as auth_router // TDD test
from fastapi.middleware.cors import CORSMiddleware


from app.sweets.routes import router as sweets_router
# from tests.test_sweets_TDD.test_routes import router as sweets_router // TDD test
# from tests.test_sweets_TDD.test_inventory import router as inventory_router // TDD test
from app.Inventory.Inventory import router as inventory_router

app = FastAPI(title="Sweet Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://uat-incubyte-sweet-shop-frontend-mxw8wbsz3.vercel.app",
        "https://uat-incubyte-sweet-shop-frontend-mc9ly2fta.vercel.app",
        "https://uat-incubyte-sweet-shop-frontend-e7ury18ql.vercel.app"
        # Add your production domain when ready
        "https://your-production-domain.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"]
)


app.include_router(user_router)
# app.include_router(auth_router) // TDD test

app.include_router(sweets_router)
app.include_router(inventory_router)
