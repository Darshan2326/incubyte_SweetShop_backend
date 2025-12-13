

from fastapi import APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute

from app.database import sweets_collection
from tests.test_auth.test_dependencies import fetch_current_user


router = APIRouter(prefix="/api/sweets", tags=["inventory"])


@router.post("/{sweetID}/purchese")
async def test_purchese(
    sweetID: str,
    # quantity: int,
    user=Depends(fetch_current_user)
):
    find_sweet = await sweets_collection.find_one({"_id": sweetID})

    if not find_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if find_sweet["quantity"] < 0:
        raise HTTPException(
            status_code=400, detail="i am sorry , Sweets are out of stock")

    await sweets_collection.update_one(
        {"_id": sweetID},
        {
            "$inc": {"quantity": -1},
            "$set": {"updatedAt": datetime.utcnow(),
                     "last_action": {
                "type": "purchese",
                "by": user["email"],
                "at": datetime.utcnow()
            }
            }
        }
    )
    return {
        "message": "congratulation Sweet purchesed successfully",
        "sweetID": sweetID
    }
