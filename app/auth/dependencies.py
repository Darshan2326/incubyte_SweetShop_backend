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


def require_admin(token=Depends(security)):
    """Dependency to check if the current user is an admin"""
    try:
        data = jwt.decode(
            token.credentials,
            JWT_SECRET,
            algorithms=["HS256"]
        )

        # Check if user has admin role
        if data.get("role") != "admin":
            raise HTTPException(
                status_code=403,
                detail="Access denied. Admin privileges required."
            )

        return data

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="something wrong >> "+str(e))
