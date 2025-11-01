from pydantic import BaseModel
from typing import Optional
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
# Ensures the database connection string is not hardcoded.
load_dotenv()

# Pull the MongoDB connection URL from environment variables
DATABASE_URL = os.getenv("DB_URL")

# Create an asynchronous MongoDB client instance
# This will handle non-blocking DB operations across the app.
client = AsyncMongoClient(DATABASE_URL)

# Connect to the target database and collection
db = client.get_database("Product_DB")
Product_collection = db.get_collection("Product")


# ---------- Pydantic Models ----------

class Product(BaseModel):
    """
    Base schema for creating a new product.
    All fields are mandatory when inserting new records.
    """
    name: str
    type: str
    stock: int


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    Fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    type: Optional[str] = None
    stock: Optional[int] = None
