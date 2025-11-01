from database.database import Product_collection
from fastapi import HTTPException
from bson import ObjectId


async def check_product(id: str):
    try:
        result = await Product_collection.find_one({"_id": ObjectId(id)})
        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


async def get_url(product: dict, file_id: str):
    try:
        return next(
            (
                metadata["url"]
                for metadata in product["image"]
                if metadata["file_id"] == ObjectId(file_id)
            ),
            None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file URL: {e}")
