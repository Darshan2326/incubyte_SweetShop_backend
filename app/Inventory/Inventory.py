from fastapi import APIRouter, Depends, HTTPException
from fastapi.routing import APIRoute
from app.database import sweets_collection
# from tests.test_auth.test_dependencies import fetch_current_user
from app.auth.dependencies import fetch_current_user, require_admin
from datetime import datetime

router = APIRouter(prefix="", tags=["inventory"])


@router.post("/api/sweets/{sweetID}/purchese")
async def purchese(
    sweetID: str,
    quantity: int,
    user=Depends(fetch_current_user)
):
    find_sweet = await sweets_collection.find_one({"_id": sweetID})

    if not find_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    if find_sweet["quantity"] < quantity:
        raise HTTPException(
            status_code=400, detail="i am sorry , Sweets are out of stock")

    hisotry = {
        "quantity": quantity,
        "type": "purchase",
        "by": user["email"],
        "at": datetime.utcnow()
    }

    await sweets_collection.update_one(
        {"_id": sweetID},
        {
            "$inc": {"quantity": -quantity},
            "$set": {"updatedAt": datetime.utcnow(),
                     "last_action": {
                "quantity": quantity,
                "type": "purchese",
                "by": user["email"],
                "at": datetime.utcnow()

            }
            },
            "$push": {"history": hisotry}
        }
    )
    return {
        "message": f"congratulation {quantity} Sweet purchesed successfully",
        "sweetID": sweetID,
        "sweet name": find_sweet["name"]

    }


@router.post("/api/sweets/{sweetID}/restock")
async def restock(
    sweetID: str,
    restoreQuantity: int,
    # Changed from fetch_current_user to require_admin
    user=Depends(require_admin)
):
    if restoreQuantity <= 0:
        raise HTTPException(status_code=400, detail="enter atleas 1 quanity")

    findSweets = await sweets_collection.find_one({"_id": sweetID})
    if not findSweets:
        raise HTTPException(
            status_code=404, detail="sweet not foud ,please check the sweetID")

    history = {
        "quantity": restoreQuantity,
        "type": "restock",
        "by": user["email"],
        "at": datetime.utcnow()
    }
    await sweets_collection.update_one(
        {"_id": sweetID},
        {
            "$inc": {"quantity": restoreQuantity},
            "$set": {"updatedAt": datetime.utcnow(),
                     "last_action": {
                "quantity": restoreQuantity,
                "type": "restock",
                "by": user["email"],
                "at": datetime.utcnow()
            }
            },
            "$push": {"history": history}
        }
    )
    return {
        "message": f"congratulation {restoreQuantity} Sweet restocked successfully",
        "sweetID": sweetID,
        "sweet name": findSweets["name"]
    }
