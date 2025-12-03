from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str = ""
    price: float
    in_stock: bool = True


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = True


class ReadProduct(BaseModel):
    id: int
    name: str
    description: str
    price: float
    in_stock: bool
    created_at: datetime
    updated_at: datetime
