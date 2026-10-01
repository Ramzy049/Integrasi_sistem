from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Model data
class Item(BaseModel):
    name: Optional[str] = None
    Umur: Optional[int] = None
    description: Optional[str] = None
    price: Optional[float] = None

# Simulasi database
items_db = {}

# ROOT
@app.get("/")
def read_root():
    return {"Undangan Pernikahan": "a day in my life"}

# CREATE (POST)
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    if item_id in items_db:
        return {"error": "Item already exists"}
    items_db[item_id] = item.dict()
    return {"message": "Item created successfully", "item": items_db[item_id]}

# READ (GET)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": items_db[item_id]}

# UPDATE (PUT)
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    # hanya field yang diisi yang akan diperbarui
    updated_data = item.dict(exclude_unset=True)
    items_db[item_id].update(updated_data)
    return {"message": "Item updated successfully", "item": items_db[item_id]}

# DELETE (DELETE)
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}