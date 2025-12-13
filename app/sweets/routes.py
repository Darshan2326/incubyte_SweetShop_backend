from fastapi import APIRouter, Depends, HTTPException
from app.sweets.model import create_sweet_model, update_sweet_model
from app.auth.dependencies import fetch_current_user, require_admin
from app.database import sweets_collection
from datetime import datetime
import uuid


router = APIRouter(prefix="", tags=["SweetsRout"])


@router.post("/api/sweets/addSweets")
async def add_Sweets(
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
async def get_sweets():
    sweets = []
    cursor = sweets_collection.find({})

    async for sweet in cursor:
        sweets.append(sweet)
    return sweets


@router.get("/api/sweets/search")
async def searchSweet(
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


@router.put("/update/{sweetID}")
async def update_sweet(
    sweetID: str,
    data: update_sweet_model,
    user=Depends(fetch_current_user)
):
    # Fixed: Using dict() instead of model_dump() for Pydantic v1.x compatibility
    updateData = data.dict(exclude_unset=True)

    if not updateData:
        raise HTTPException(
            status_code=400,
            detail=">>> No data provided for update please provide data <<< "
        )

    updateData["updatedAt"] = datetime.utcnow()

    result = await sweets_collection.update_one(
        {"_id": sweetID},
        {"$set": updateData}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail=">>> Sweet not found <<< please check the ID and try again"
        )

    return {
        "message": "Sweet updated successfully check all sweet for see the update",
        "sweetID": sweetID,
        "updated_fields": updateData
    }


@router.delete("/delete/{sweetID}")
async def delete_sweet(
    sweetID: str,
    user=Depends(require_admin)
):
    # First find the sweet to get its name before deleting
    sweet = await sweets_collection.find_one({"_id": sweetID})
    if not sweet:
        raise HTTPException(
            status_code=404,
            detail=">>> Sweet not found <<< please check the ID and try again"
        )

    result = await sweets_collection.delete_one({"_id": sweetID})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=">>> Sweet not found <<< please check the ID and try again"
        )
    return {
        "message": ">>> Sweet deleted successfully <<<",
        "sweetID": sweetID,
        "sweetName": sweet["name"]
    }
