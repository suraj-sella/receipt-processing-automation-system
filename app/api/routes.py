"""API routes for receipt processing application."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from app.models.receipt_file import ReceiptFile
from app.utils.database import SessionLocal
import os
from datetime import datetime
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from app.models.receipt import Receipt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

def extract_text_from_pdf_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def parse_amount(amount):
    if amount is None:
        return None
    try:
        # Remove $ and spaces, then convert to float
        return float(str(amount).replace('$', '').replace(',', '').strip())
    except Exception:
        return None

@router.post("/process")
def process_file(file_id: int = Body(..., embed=True)):
    """
    Extract receipt details using OCR and store in the database.
    """
    db = SessionLocal()
    try:
        db_file = db.query(ReceiptFile).filter(ReceiptFile.id == file_id).first()
        if not db_file or not db_file.is_valid:
            raise HTTPException(status_code=404, detail="Valid file not found")
        
        # Extract text from PDF using OCR (Tesseract)
        try:
            text = extract_text_from_pdf_with_ocr(db_file.file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OCR failed: {e}")

        # Use OpenAI (or your existing function) to extract structured fields
        fields = extract_with_gpt(text)
        merchant = fields.get("merchant_name")
        total = parse_amount(fields.get("total_amount"))
        date = fields.get("date")

        # Store in receipt table
        receipt = Receipt(
            purchased_at=None,  # You can parse date if you want
            merchant_name=merchant,
            total_amount=total,
            file_path=db_file.file_path
        )
        db.add(receipt)
        db_file.is_processed = True
        db.commit()
        db.refresh(receipt)

        return {
            "receipt_id": receipt.id,
            "merchant_name": merchant,
            "total_amount": total,
            "raw_text": text[:500]  # Show a snippet of extracted text
        }
    finally:
        db.close()
        
def extract_with_gpt(raw_text):
    prompt = f"""
You are an intelligent receipt parser. Extract the following fields from the receipt text below:
- merchant_name
- total_amount
- date (if available)

If a field is missing, return null for it.

Receipt text:
\"\"\"
{raw_text}
\"\"\"

Return your answer as a JSON object with keys: merchant_name, total_amount, date.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0
    )
    import json
    try:
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"merchant_name": None, "total_amount": None, "date": None, "error": str(e)}