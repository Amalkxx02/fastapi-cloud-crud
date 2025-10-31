from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel,EmailStr
from typing import Optional
from pymongo import mongo_client

client = mongo_client("")
db = client[""]

class UserAdd(BaseModel):
    user_name:str
    user_email: EmailStr
    user_password:str
    