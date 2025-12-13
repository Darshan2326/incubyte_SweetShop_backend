# import pytest
# from unittest.mock import AsyncMock, patch
# from datetime import datetime
# import uuid
# from tests.test_sweets_TDD.test_model import create_sweet_model
# from app.auth.dependencies import fetch_current_user
# from app.database import sweets_collection


# @pytest.mark.asyncio
# async def test_add_sweets_success():
#     """Test successful addition of sweets"""
#     # Create a mock sweet data
#     mock_sweet_data = create_sweet_model(
#         name="Chocolate Cake",
#         category="Cakes",
#         price=15.99,
#         quantity=10
#     )

#     # Mock user data
#     mock_user = {"id": "test-user-id", "email": "test@example.com"}

#     # Mock database operations
#     with patch('uuid.uuid4', return_value="test-sweet-id"):
#         with patch('datetime.datetime') as mock_datetime:
#             mock_datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)

#             with patch('app.database.sweets_collection.insert_one', new=AsyncMock()) as mock_insert:
#                 # Call the actual route handler function
#                 # Note: Since the original function is not properly structured,
#                 # we'll create a proper test for the intended functionality

#                 # For now, we'll just test that the logic would work correctly
#                 sweet_id = str(uuid.uuid4())

#                 sweet_data = {
#                     "_id": sweet_id,
#                     "name": mock_sweet_data.name,
#                     "category": mock_sweet_data.category,
#                     "price": mock_sweet_data.price,
#                     "quantity": mock_sweet_data.quantity,
#                     "creator": mock_user["id"],
#                     "createdAt": datetime.utcnow(),
#                     "updatedAt": None
#                 }

#                 # Verify the data structure is correct
#                 assert sweet_data["_id"] == sweet_id
#                 assert sweet_data["name"] == "Chocolate Cake"
#                 assert sweet_data["creator"] == "test-user-id"

#                 # Verify insert would be called
#                 # In a real test, you would actually call the route function
#                 assert True  # Placeholder assertion


# @router.get("/api/sweets")
# async def test_get_sweets():

#     sweets = []

#     cursor = sweets_collection.find({})

#     async for sweet in cursor:

#         sweets.append(sweet)

#     return sweets


# @router.get("/api/sweets/search")
# async def test_searchSweet(

#     name: str | None = None,

#     category: str | None = None,

#     low_price: float | None = None,

#     hight_price: float | None = None,

#     user=Depends(fetch_current_user)

# ):

#     sweetsList = {}

#     if name:

#         sweetsList["name"] = {"$regex": name, "$options": "i"}

#     if category:

#         sweetsList["category"] = {"$regex": category, "$options": "i"}

#     if low_price is not None or hight_price is not None:

#         sweetsList["price"] = {}

#         if low_price is not None:

#             sweetsList["price"]["$gte"] = low_price

#         if hight_price is not None:

#             sweetsList["price"]["$lte"] = hight_price

#     sweets = []

#     cursor = sweets_collection.find(sweetsList)

#     async for sweet in cursor:

#         sweets.append(sweet)

#     return sweets


from fastapi import APIRouter, Depends, HTTPException
# from app.sweets.model import create_sweet_model
from tests.test_sweets_TDD.test_model import create_sweet_model
from app.auth.dependencies import fetch_current_user
from app.database import sweets_collection
from datetime import datetime
import uuid


router = APIRouter(prefix="", tags=["SweetsRout"])


@router.post("/api/sweets/addSweets")
async def test_add_Sweets(
    data: create_sweet_model,
    user=Depends(fetch_current_user)
):
    sweetID = str(uuid.uuid4())

    sweet_data = {
        "_id": sweetID,
        "name": data.name,
        "category": data.category,
        "price":  data.price,
        "quantity": data.quantity,
        "creator": user["id"],
        "createdAt": datetime.utcnow(),
        # "updated_at" : datetime.utcnow(),
        "updatedAt": None
    }

    await sweets_collection.insert_one(sweet_data)

    return {
        "message": "new sweet added successfully",
        "sweet": sweet_data
    }


@router.get("/api/sweets")
async def test_get_sweets():
    sweets = []
    cursor = sweets_collection.find({})

    async for sweet in cursor:
        sweets.append(sweet)
    return sweets


@router.get("/api/sweets/search")
async def test_searchSweet(
    name: str | None = None,
    category: str | None = None,
    low_price: float | None = None,
    hight_price: float | None = None,
    user=Depends(fetch_current_user)
):
    sweetsList = {}

    if name:
        sweetsList["name"] = {"$regex": name, "$options": "i"}
    if category:
        sweetsList["category"] = {"$regex": category, "$options": "i"}

    if low_price is not None or hight_price is not None:
        sweetsList["price"] = {}
        if low_price is not None:
            sweetsList["price"]["$gte"] = low_price
        if hight_price is not None:
            sweetsList["price"]["$lte"] = hight_price

    sweets = []
    cursor = sweets_collection.find(sweetsList)
    async for sweet in cursor:
        sweets.append(sweet)
    return sweets
