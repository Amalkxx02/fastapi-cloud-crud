from database.database import Product_collection
from fastapi import HTTPException
from bson import ObjectId


async def check_product(id: str):
    """
    Verify if a product exists in the database.

    Args:
        id (str): The ObjectId of the product as a string.

    Returns:
        dict: The product document if found.

    Raises:
        HTTPException:
            - 404 if the product doesn't exist.
            - 500 for any unexpected database errors.
    """
    try:
        result = await Product_collection.find_one({"_id": ObjectId(id)})
        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


async def get_url(product: dict, file_id: str):
    """
    Retrieve the file URL for a given file ID from a product document.

    Args:
        product (dict): The product document containing file metadata.
        file_id (str): The file's ObjectId as a string.

    Returns:
        str | None: The URL of the file if found, otherwise None.

    Raises:
        HTTPException:
            - 500 if an unexpected error occurs during lookup.
    """
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
