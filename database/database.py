from pydantic import BaseModel
from typing import Optional
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
client = AsyncMongoClient(DATABASE_URL)

db = client.get_database("Product_DB")
Product_collection = db.get_collection("Product")

class ProductMetadataUpdate(BaseModel):
    url:Optional[str] = None
    name:Optional[str] = None
    size:Optional[str] = None
    type:Optional[str] = None

class Product(BaseModel):
    name:str
    type: str
    stock:int
    
class ProductUpdate(BaseModel):
    name:Optional[str] = None
    type: Optional[str] = None
    stock:Optional[int] = None