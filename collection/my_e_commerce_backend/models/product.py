from datetime import datetime
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from ..utilities.database import engine


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: str = ""
    price: float
    in_stock: bool = True

    is_active: bool = True
    created_at: datetime
    updated_at: datetime


def init_product_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
