from fastapi import HTTPException, UploadFile
from bson import ObjectId
import os


async def add_file(file: UploadFile, file_id: str = None):
    """
    Save an uploaded file to local storage and return its metadata.

    Args:
        file (UploadFile): The incoming file object from FastAPI.
        file_id (str, optional): Existing ObjectId to reuse (mostly for updates).

    Returns:
        dict: Metadata containing file_id, name, size, type, and storage URL.

    Raises:
        HTTPException:
            - 400 if the file cannot be received or written to disk.
    """
    try:
        with open(f"file/{file.filename}", "wb") as buffer:
            content = await file.read()
            url = f"file/{file.filename}"
            size = len(content)
            buffer.write(content)
    except Exception:
        raise HTTPException(status_code=400, detail="File not received")

    file_obj_id = ObjectId(file_id) if file_id else ObjectId()

    metadata = {
        "file_id": file_obj_id,
        "url": url,
        "name": file.filename,
        "size": size,
        "type": file.content_type,
    }
    return metadata


def remove_file(url: str):
    """
    Delete a file from local storage if it exists.

    Args:
        url (str): Path or URL of the file to remove.

    Notes:
        Logs an error message if deletion fails instead of raising.
    """
    try:
        if os.path.exists(url):
            os.remove(url)
    except Exception as e:
        print(f"OS error: {e}")
