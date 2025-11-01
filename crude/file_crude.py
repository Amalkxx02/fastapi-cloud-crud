from fastapi import APIRouter, HTTPException, UploadFile, File
from bson import ObjectId
from utils.file import remove_file, add_file
from utils.db import check_product, get_url
from database.database import Product_collection

router = APIRouter(prefix="/files", tags=["File"])


@router.get("/all/{product_id}")
async def get_all_file(product_id: str):
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
    if not doc:
        return None
    doc["file_id"] = str(doc["file_id"])
    return doc
