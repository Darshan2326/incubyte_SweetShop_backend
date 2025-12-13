
from fastapi import APIRouter, Depends, HTTPException
# from app.sweets.model import create_sweet_model
from tests.test_sweets_TDD.test_model import create_sweet_model, update_sweet_model
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


@router.put(f"/{sweetID}")
async def test_update_sweet(
    sweetID: str,
    data: update_sweet_model,
    user=Depends(fetch_current_user)
):
    updateData = data.model_dump(exclude_unset=True)

    if not updateData:
        raise HTTPException(
            status_code=400, detail="No data provided for update please provude data")

    updateData["updatedAt"] = datetime.utcnow()

    result = await sweets_collection.update_one({"_id": sweetID}, {"$set": updateData})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Sweet not found of this ID or not updated please check the ID and try again")
    return {"message": "Sweet updated successfully", "sweet": updateData}
