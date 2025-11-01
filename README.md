FastAPI + MongoDB CRUD Application
Overview

This project is a backend API built with FastAPI and MongoDB. It manages products with full CRUD operations and supports file uploads linked to each product. The goal was to keep it modular and ready for cloud integration.

Features
FastAPI backend with async endpoints.
MongoDB as the main database for products and file metadata.
CRUD operations for creating, reading, updating, and deleting products.
File upload support — each file’s URL, name, size, and type are stored in MongoDB.
Files are currently stored locally due to account setup limitations for AWS/DigitalOcean.

Note
Cloud storage (AWS S3 or DigitalOcean Spaces) isn’t used yet because those platforms need verified accounts.
Files are saved locally, but the system is already structured to switch to cloud storage later.

Setup
Add your MongoDB connection string in .env under DB_URL.
Make sure Python 3.10+ is installed.
Install dependencies after setting up your environment (see below).
Run the app and open /docs or /redoc to test the API.

Run Locally
Create a virtual environment:
-python -m venv venv
Install dependencies:
-pip install -r requirements.txt
Start the server:
-uvicorn app.main:app --reload

Deployment
Docker: Containerization is planned but not yet finalized.
Cloud: Hosting will be on GCP Cloud Run later.

Future Plans
Integrate AWS S3 / DigitalOcean Spaces for file storage.
Improve logging and error tracking.

Example Usage
Create a product with name, type, and stock.
Upload one or more files to that product.
Fetch product data along with file info.
Update or delete files/products when needed.