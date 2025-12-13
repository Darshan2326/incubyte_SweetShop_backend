
from fastapi import APIRouter, Depends, HTTPException
from app.sweets.model import create_sweet_model


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

    await create_sweet_model.insert_one(sweet_data)

    return {
        "message": "new sweet added successfully",
        "sweet": sweet_data
    }
