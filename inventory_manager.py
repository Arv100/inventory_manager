from fastapi import FastAPI, Path
from datetime import datetime
from db_manager import client_connection
from pydantic import BaseModel
from typing import Optional

class item(BaseModel):
    item_name : str
    item_price : Optional[int] = None
    item_quantity :Optional[int] = None
    item_brand :Optional[str] = None
    inserted_timestamp : Optional[datetime] = None

app = FastAPI()

client = client_connection()
db = client['inventory_manager']
inventory = db['inventory']  

@app.get('/')
def home():
    return  "Welcome to inventory manager"

@app.get('/get-all-items')
def get_all_items():
    result = list(inventory.find({},{"_id" : 0}))
    if len(result) > 0:
        return result
    return {"collection" : "Empty"}

@app.get('/find-items-by-name/{item_name}')
def find_items_by_name(item_name :str = Path(description='Name of the item',min_length=1)):
    result = list(inventory.find({"item_name" : item_name}, {"_id": 0}))
    if len(result) > 0:
        return list(result)
    return {item_name : "Not found"}

@app.get('/find-items-by-brand/{brand_name}')
def find_items_by_brand(brand_name :str = Path(description='Name of the brand',min_length=1)):
    result = list(inventory.find({"item_brand" : brand_name}, {"_id": 0}))
    if len(result) > 0:
        return result
    return {brand_name : "Not found"}

@app.post('/insert-items')
def insert_items(data :item):
    if not data.inserted_timestamp:
        data.inserted_timestamp = datetime.now()

    result = inventory.find_one({"item_name" : data.item_name,"item_brand" : data.item_brand})
    if result:
        return {"Item" : "Already present"}

    result = inventory.insert_one(data.model_dump())
    return {"inserted_id": str(result.inserted_id)}

@app.put('/update-item')
def update_item(data :item):
    if inventory.find_one({"item_name" : data.item_name}):
        data.inserted_timestamp = datetime.now()
        inventory.update_one({"item_name" : data.item_name},{"$set" : {"inserted_timestamp" : data.inserted_timestamp}})
        if data.item_brand:
            inventory.update_one({"item_name" : data.item_name},{"$set" : {"item_brand" : data.item_brand}})
        if data.item_price:
            inventory.update_one({"item_name" : data.item_name},{"$set" : {"item_price" : data.item_price}})
        if data.item_quantity:
            inventory.update_one({"item_name" : data.item_name},{"$set" : {"item_quantity" : data.item_quantity}})
        return {"update" : "successful"}
    else:
        return {"Item_name" : "not present"}

@app.delete('/delete-item/{item_name}')
def delete_item(item_name :str = Path(description="Provide the item name to delete")):
    if inventory.find_one({"item_name" : item_name}):
        inventory.delete_one({"item_name" : item_name})
        return {"delete" : "successfull"}
    return {"item_name" : "Not present"}
    