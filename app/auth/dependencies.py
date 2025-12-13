from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from app.user.utils import JWT_SECRET

security = HTTPBearer()


def fetch_current_user(token=Depends(security)):
    try:
        data = jwt.decode(
            token.credentials,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        return data

    except Exception as e:
        raise HTTPException(
            status_code=401, detail="something wrong >> "+str(e))
