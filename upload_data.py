import json
import math
from pymongo import MongoClient

def clean_nan_values(obj):
    if isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(item) for item in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    elif obj == "NaN":
        return None
    return obj

# MongoDB connection
client = MongoClient("mongodb+srv://mashmelo1969_db_user:password@cluster0.v4o9qyt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.recipe_db
collection = db.recipes

# Load and clean JSON data
with open("US_recipes_null.Pdf.json", "r") as file:
    data = json.load(file)
    data = clean_nan_values(data)
    
if isinstance(data, list):
    collection.insert_many(data)
    print(f"Uploaded {len(data)} recipes")
else:
    collection.insert_one(data)
    print("Uploaded 1 recipe")

print(f"Total recipes in database: {collection.count_documents({})}")
