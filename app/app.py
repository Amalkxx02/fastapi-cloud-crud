from fastapi import FastAPI
from crude import product_crude, file_crude

# Initialize the main FastAPI application
# This acts as the entry point for all routes defined in submodules.
app = FastAPI(
    title="Product Management API",
    description=(
        "A FastAPI-based backend handling product data and file operations. "
        "Endpoints are modularized for better structure and scalability."
    ),
    version="1.0.0"
)

# Include the router responsible for product-related CRUD operations.
# Handles product creation, retrieval, updating, and deletion.
app.include_router(product_crude.router)

# Include the router responsible for handling file-related logic.
# Deals with file uploads, metadata management, and related operations.
app.include_router(file_crude.router)
