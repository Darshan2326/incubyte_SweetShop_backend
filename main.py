from fastapi import FastAPI
# from app.auth.routes import router as auth_router
from app.user.routes import router as user_router
# from test.auth_TDD import router as auth_router // TDD test


from app.sweets.routes import router as sweets_router
# from tests.test_sweets_TDD.test_routes import router as sweets_router // TDD test
# from tests.test_sweets_TDD.test_inventory import router as inventory_router // TDD test
from app.Inventory.Inventory import router as inventory_router

app = FastAPI(title="Sweet Shop API")

app.include_router(user_router)
# app.include_router(auth_router) // TDD test

app.include_router(sweets_router)
app.include_router(inventory_router)
