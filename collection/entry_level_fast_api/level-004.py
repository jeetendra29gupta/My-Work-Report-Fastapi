from typing import Optional, Dict
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, UUID4

app = FastAPI()


class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True
    rating: Optional[int] = None


class Items(ItemCreate):
    id: UUID4


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    rating: Optional[int] = None


items_db: Dict[UUID4, Items] = {}


# Create
@app.post("/items")
def create_item(item: ItemCreate):
    new_item = item.model_dump()
    new_item["id"] = uuid4()
    items_db[new_item.id] = new_item
    return new_item


# Read All
@app.get("/items")
def read_all_items():
    return list(items_db.values())


# Read One
@app.get("/items/{item_id}")
def read_item(item_id: UUID4):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


# Update (Full)
@app.put("/items/{item_id}")
def update_item(item_id: UUID4, updated_data: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = Items(id=item_id, **updated_data.dict())
    items_db[item_id] = updated_item
    return updated_item


# Update (Partial)
@app.patch("/items/{item_id}")
def partial_update_item(item_id: UUID4, item_update: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    existing_item = items_db[item_id]
    updated_fields = item_update.dict(exclude_unset=True)
    updated_item = existing_item.copy(update=updated_fields)

    items_db[item_id] = updated_item
    return updated_item


# Delete
@app.delete("/items/{item_id}")
def delete_item(item_id: UUID4):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return {"deleted": deleted_item}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8181)
