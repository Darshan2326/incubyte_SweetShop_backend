from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

DEMO_ADMIN_USER = {
    "id": "demo-admin-id",
    "email": "admin@demo.com",
    "role": "admin",
    "name": "Admin User"
}

def fetch_current_user(token=Depends(security)):
    if token.credentials != "demo-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return DEMO_ADMIN_USER


def require_admin(token=Depends(security)):
    if token.credentials != "demo-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return DEMO_ADMIN_USER
