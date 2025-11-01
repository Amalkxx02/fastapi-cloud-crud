from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
from utils.file import remove_file, add_file
from utils.db import check_product, get_url
from database.database import Product_collection

# Router setup for all file-related endpoints.
# Handles upload, retrieval, update, and deletion of files tied to a product.
router = APIRouter(prefix="/files", tags=["File"])


@router.get("/all/{product_id}")
async def get_all_file(product_id: str):
    """
    Fetch all files linked to a specific product.

    Args:
        product_id (str): The ID of the product.

    Returns:
        list: A list of serialized file metadata objects.

    Raises:
        HTTPException: If the product doesn't exist or the DB query fails.
    """
    await check_product(product_id)

    try:
        result = await Product_collection.find_one(
            {"_id": ObjectId(product_id)}, {"image": 1}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return [serialize_file(file) for file in result["image"]]


@router.get("/single/{product_id}")
async def get_file(product_id: str, file_id: str):
    """
    Get a specific file from a product using its file_id.

    Args:
        product_id (str): Product’s unique ID.
        file_id (str): File’s unique ID.

    Returns:
        dict: The serialized file metadata.

    Raises:
        HTTPException: For invalid product, missing file, or DB errors.
    """
    await check_product(product_id)

    try:
        result = await Product_collection.find_one(
            {"_id": ObjectId(product_id)},
            {"image": {"$elemMatch": {"file_id": ObjectId(file_id)}}},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return serialize_file(result["image"][0])


@router.post("/{product_id}")
async def upload_file(product_id: str, file: UploadFile = File(...)):
    """
    Upload a new file and attach it to a product.

    Handles:
        - Saving the file (via utils)
        - Storing metadata in MongoDB
        - Cleanup if DB operation fails

    Args:
        product_id (str): Product’s unique ID.
        file (UploadFile): The uploaded file.

    Returns:
        dict: Success message with status.

    Raises:
        HTTPException: If upload or DB update fails.
    """
    await check_product(product_id)

    file_metadata = await add_file(file)

    try:
        result = await Product_collection.update_one(
            {"_id": ObjectId(product_id)}, {"$addToSet": {"image": file_metadata}}
        )
    except Exception as e:
        remove_file(file_metadata["url"])
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if result.modified_count == 0:
        remove_file(file_metadata["url"])
        raise HTTPException(status_code=400, detail="File could not be saved")

    return {"status": 200, "detail": "File saved successfully"}


@router.patch("/{product_id}")
async def update_file(product_id: str, file_id: str, file: UploadFile = File(...)):
    """
    Replace an existing file with a new one for the same product.

    Handles:
        - Upload of new file
        - Removal of old file from storage
        - Update of metadata in DB

    Args:
        product_id (str): Product’s unique ID.
        file_id (str): The existing file’s ID.
        file (UploadFile): New file to upload.

    Returns:
        dict: Success message with status.

    Raises:
        HTTPException: On missing product, DB failure, or invalid file ID.
    """
    product = await check_product(product_id)
    old_url = await get_url(product, file_id)
    file_metadata = await add_file(file)

    try:
        result = await Product_collection.update_one(
            {"_id": ObjectId(product_id), "image.file_id": ObjectId(file_id)},
            {"$set": {"image.$": file_metadata}},
        )
        if old_url:
            remove_file(old_url)
    except Exception as e:
        remove_file(file_metadata["url"])
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if result.modified_count == 0:
        remove_file(file_metadata["url"])
        raise HTTPException(status_code=404, detail="File not found")

    return {"status": 200, "detail": "File updated successfully"}


@router.delete("/{product_id}")
async def delete_file(product_id: str, file_id: str):
    """
    Delete a file from a product’s image list.

    Args:
        product_id (str): Product’s unique ID.
        file_id (str): File’s unique ID.

    Returns:
        dict: Status message on success.

    Raises:
        HTTPException: If the file or product doesn’t exist, or DB fails.
    """
    product = await check_product(product_id)
    url = await get_url(product, file_id)

    if not url:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        result = await Product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$pull": {"image": {"file_id": ObjectId(file_id)}}},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="File not found")

    remove_file(url)
    return {"status": 200, "detail": "File deleted successfully"}


def serialize_file(doc):
    """
    Convert MongoDB file document to a JSON-safe dict.

    Args:
        doc (dict): Raw MongoDB document.

    Returns:
        dict | None: Cleaned document with stringified ObjectId.
    """
    if not doc:
        return None
    doc["file_id"] = str(doc["file_id"])
    return doc
