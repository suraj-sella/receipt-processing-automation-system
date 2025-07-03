from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.receipt_file import ReceiptFile
from app.utils.database import SessionLocal
import os
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a receipt file (PDF format)
    """
    # Check if file is PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Save to database
    db = SessionLocal()
    try:
        db_receipt_file = ReceiptFile(
            file_name=file.filename,
            file_path=file_path,
            is_valid=False,  # We'll validate this later
            is_processed=False
        )
        db.add(db_receipt_file)
        db.commit()
        db.refresh(db_receipt_file)
        
        return {
            "message": "File uploaded successfully",
            "file_id": db_receipt_file.id,
            "file_name": file.filename
        }
    finally:
        db.close()