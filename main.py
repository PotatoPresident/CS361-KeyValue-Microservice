import json
import os
import uuid
from typing import Dict, Any

from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel

app = FastAPI(title="JSON Key-Value Store")

DATA_DIR = "data_store"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_file_path(key: str) -> str:
    safe_key = key.replace('/', '_').replace('\\', '_')
    return os.path.join(DATA_DIR, f"{safe_key}.json")


def save_item(key: str, value: Any) -> None:
    file_path = get_file_path(key)
    with open(file_path, 'w') as f:
        json.dump(value, f)


def load_item(key: str) -> Any:
    file_path = get_file_path(key)
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as f:
        return json.load(f)

def delete_item_file(key: str) -> bool:
    file_path = get_file_path(key)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

class Item(BaseModel):
    value: Any

class ItemResponse(BaseModel):
    key: str
    value: Any

class ErrorResponse(BaseModel):
    message: str

@app.post("/store/{key}", status_code=status.HTTP_201_CREATED)
async def upsert_item(key: str, item: Item, response: Response) -> None:
    save_item(key, item.value)

@app.get("/store/{key}", status_code=status.HTTP_200_OK)
async def read_item(key: str) -> Item:
    value = load_item(key)
    if value is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return Item(value=value)

@app.delete("/store/{key}", status_code=status.HTTP_200_OK)
async def delete_item(key: str) -> None:
    if not delete_item_file(key):
        raise HTTPException(status_code=404, detail="Item not found")
