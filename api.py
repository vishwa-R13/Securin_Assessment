from pymongo import MongoClient
from fastapi import FastAPI, Query
from bson import ObjectId
from typing import Optional
import uvicorn
import re

# MongoDB connection
client = MongoClient("mongodb+srv://mashmelo1969_db_user:ImG7lh65WUYud9nn@cluster0.v4o9qyt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recipe_db
collection = db.recipes

# FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Recipe API"}

@app.get("/api/recipes")
def get_recipes(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * limit
    
    recipes = list(collection.find({}).sort("rating", -1).skip(skip).limit(limit))
    total = collection.count_documents({})
    
    # Convert ObjectId to string
    for recipe in recipes:
        recipe["id"] = str(recipe["_id"])
        del recipe["_id"]
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": recipes
    }

@app.get("/api/recipes/search")
def search_recipes(
    calories: Optional[str] = None,
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    total_time: Optional[str] = None,
    rating: Optional[str] = None
):
    query = {}
    
    # Title search (partial match)
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    
    # Cuisine filter
    if cuisine:
        query["cuisine"] = cuisine
    
    # Numeric filters with operators
    for field, value in [("calories", calories), ("total_time", total_time), ("rating", rating)]:
        if value:
            if match := re.match(r"(>=|<=|>|<|=?)([0-9.]+)", value):
                operator, num = match.groups()
                num = float(num)
                if operator == ">=":
                    query[field] = {"$gte": num}
                elif operator == "<=":
                    query[field] = {"$lte": num}
                elif operator == ">":
                    query[field] = {"$gt": num}
                elif operator == "<":
                    query[field] = {"$lt": num}
                else:
                    query[field] = num
    
    recipes = list(collection.find(query))
    
    # Convert ObjectId to string
    for recipe in recipes:
        recipe["id"] = str(recipe["_id"])
        del recipe["_id"]
    
    return {"data": recipes}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)