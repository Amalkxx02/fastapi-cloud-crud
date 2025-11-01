from fastapi import APIRouter, HTTPException
from bson import ObjectId
from utils.db import check_product
from database.database import Product, ProductUpdate, Product_collection

# Router setup for product operations.
# Handles creating, reading, updating, and deleting product data.
router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/")
async def upload_product(product: Product):
    """
    Create a new product entry in the database.

    Args:
        product (Product): Product data validated by Pydantic.

    Returns:
        str: The inserted product's ObjectId as a string.

    Raises:
        HTTPException: 
            - 409 if the product already exists.
            - 500 for any database errors.
    """
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
    """
    Retrieve all products from the database.

    Returns:
        list: A list of all products with serialized IDs.

    Raises:
        HTTPException: If a database error occurs.
    """
    try:
        products = await Product_collection.find().to_list(length=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return [serialize_doc(p) for p in products]


@router.get("/{product_id}", response_model=None)
async def get_product(product_id: str):
    """
    Get a single product by its ID.

    Args:
        product_id (str): The ObjectId of the product.

    Returns:
        dict: Serialized product document.

    Raises:
        HTTPException: 
            - 404 if not found.
            - 500 for DB errors.
    """
    product = await check_product(product_id)
    return serialize_doc(product)


@router.patch("/{product_id}")
async def update_product(product_id: str, product: ProductUpdate):
    """
    Update specific fields of a product.

    Args:
        product_id (str): The product’s ObjectId.
        product (ProductUpdate): Fields to update.

    Returns:
        dict: Success message on completion.

    Raises:
        HTTPException: 
            - 400 if nothing is updated.
            - 500 for DB errors.
    """
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
    """
    Delete a product by its ID.

    Args:
        product_id (str): The ObjectId of the product to delete.

    Returns:
        dict: Confirmation message upon successful deletion.

    Raises:
        HTTPException:
            - 404 if the product doesn't exist.
            - 500 for any DB errors.
    """
    try:
        product = await Product_collection.delete_one({"_id": ObjectId(product_id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if product.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"detail": "Product deleted successfully"}


def serialize_doc(doc):
    """
    Convert a MongoDB document into a JSON-friendly format.

    Args:
        doc (dict): MongoDB document.

    Returns:
        dict | None: Cleaned document with stringified _id.
    """
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc
