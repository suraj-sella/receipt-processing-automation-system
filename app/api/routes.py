from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from app.models.receipt_file import ReceiptFile
from app.utils.database import SessionLocal
import os
from datetime import datetime
from PyPDF2 import PdfReader

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

@router.post("/validate")
def validate_file(file_id: int = Body(..., embed=True)):
    """
    Validate whether the uploaded file is a valid PDF.
    """
    db = SessionLocal()
    try:
        db_file = db.query(ReceiptFile).filter(ReceiptFile.id == file_id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Try to open the file as a PDF
        try:
            with open(db_file.file_path, "rb") as f:
                PdfReader(f)
            db_file.is_valid = True
            db_file.invalid_reason = None
        except Exception as e:
            db_file.is_valid = False
            db_file.invalid_reason = str(e)
        
        db.commit()
        db.refresh(db_file)
        return {
            "file_id": db_file.id,
            "is_valid": db_file.is_valid,
            "invalid_reason": db_file.invalid_reason
        }
    finally:
        db.close()