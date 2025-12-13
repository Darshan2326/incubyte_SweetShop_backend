from typing import Optional
from pydantic import BaseModel


class create_sweet_model(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class update_sweet_model(BaseModel):
    name: Optional[str] = None
    catagory: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
