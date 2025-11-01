from fastapi import HTTPException,UploadFile
from bson import ObjectId
import os

async def add_file(file:UploadFile,file_id:str = None):
    try:
        with open(f"file/{file.filename}", "wb") as buffer:
            content = await file.read()
            url = f"file/{file.filename}"
            size = len(content)
            buffer.write(content)
    except:
        raise HTTPException(status_code=400, detail=("file not received"))
    
    file_obj_id = ObjectId(file_id) if file_id else ObjectId()

    metadata = {
        "file_id":file_obj_id,
        "url": url,
        "name": file.filename,
        "size": size,
        "type": file.content_type,
    }
    return metadata

def remove_file(url):
    try:
        if os.path.exists(url):
            os.remove(url)
    except Exception as e:
        print(f"Os error {e}")