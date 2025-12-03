from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory database
items_db = []


# Pydantic model for item data with ID field UUID


class Item(BaseModel):
    name: str
    price: float


# Create an item
@app.post("/items/", response_model=dict)
async def create_item(item: Item):
    item_data = item.model_dump()
    item_data["id"] = str(uuid4())
    items_db.append(item_data)
    return item_data


# Get all items
@app.get("/items/", response_model=list[dict])
async def get_items():
    return items_db


# Get an item by ID
@app.get("/items/{item_id}", response_model=dict)
async def get_item(item_id: str):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}


# Update an item by ID
@app.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: str, updated_item: Item):
    for item in items_db:
        if item["id"] == item_id:
            item.update(updated_item.model_dump())
            return item
    return {"error": "Item not found"}


# Delete an item by ID
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    for item in items_db:
        if item["id"] == item_id:
            items_db.remove(item)
            return {"message": "Item deleted"}
    return {"error": "Item not found"}
