from fastapi import APIRouter, HTTPException
from bson import ObjectId
from utils.db import check_product
from database.database import Product, ProductUpdate, Product_collection

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/")
async def upload_product(product: Product):

    product = product.model_dump()
    try:
        exist = await Product_collection.find_one({"name": product["name"]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if exist:
        raise HTTPException(status_code=409, detail="Product already exists")

    try:
        result = await Product_collection.insert_one(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return str(result.inserted_id)


@router.get("/", response_model=None)
async def get_all_product():
    try:
        products = await Product_collection.find().to_list(length=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return [serialize_doc(p) for p in products]


@router.get("/{product_id}", response_model=None)
async def get_product(product_id: str):
    product = await check_product(product_id)
    return serialize_doc(product)


@router.patch("/{product_id}")
async def update_product(product_id: str, product: ProductUpdate):

    await check_product(product_id)

    product = product.model_dump()
    update_data = {k: v for k, v in product.items() if v is not None}

    try:
        result = await Product_collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No fields were updated")

    return {"status": 200, "detail": "Product updated successfully"}


@router.delete("/{product_id}")
async def delete_product(product_id: str):
    try:
        product = await Product_collection.delete_one({"_id": ObjectId(product_id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if product.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"detail": "Product deleted successfully"}


def serialize_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc
