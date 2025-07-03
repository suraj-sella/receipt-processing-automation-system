# Automate Accounts Receipt Processing API

## 🚀 Overview
This project is a web application for automating the extraction of key details from scanned receipt PDFs using OCR (Tesseract) and AI (OpenAI GPT). It provides REST APIs to upload, validate, process, and retrieve receipt data, storing everything in a SQLite database.

---

## 📦 Features
- Upload scanned receipts (PDF)
- Validate PDF files
- Extract receipt details using OCR and AI
- Store and manage extracted data in SQLite
- RESTful API for managing and retrieving receipts

---

## 🛠️ Technology Stack
- **Backend:** Python 3.8+
- **Web Framework:** FastAPI
- **Database:** SQLite (via SQLAlchemy)
- **OCR:** Tesseract OCR (via pytesseract, pdf2image)
- **AI Extraction:** OpenAI GPT (gpt-3.5-turbo or gpt-4)
- **PDF Processing:** PyPDF2, pdf2image
- **Other:** python-dotenv, Pillow

---

## 📋 Dependencies
Install these Python packages (see `requirements.txt`):

```
fastapi
uvicorn
sqlalchemy
pydantic
python-multipart
pillow
pytesseract
openai
python-dotenv
pytest
PyPDF2
pdf2image
```

**System dependencies:**
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (add to PATH)
- [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/) (add `bin` to PATH)

---

## 🖥️ Setup Instructions

1. **Clone the repository and enter the code directory:**
   ```bash
   git clone <your-repo-url>
   cd automate-accounts/code
   ```

2. **Install Python dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Install Tesseract OCR and Poppler:**
   - Download and install Tesseract OCR and Poppler (see links above).
   - Add their `bin` folders to your system PATH.

4. **Set up environment variables:**
   - Copy or edit `config.env`:
     ```env
     DATABASE_URL=sqlite:///./database/receipts.db
     UPLOAD_DIR=./uploads
     OPENAI_API_KEY=sk-...  # Your OpenAI API key
     MAX_FILE_SIZE=10485760
     ```

5. **Initialize the database:**
   ```bash
   python -m app.utils.init_db
   ```

6. **Run the server:**
   ```bash
   python run_server.py
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000)

7. **Access API docs:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧑‍💻 API Usage

### 1. **Upload Receipt**
**POST** `/api/v1/upload`
- Upload a PDF receipt file.
- **Request:**
  - Form-data: `file` (PDF)
- **Response:**
```json
{
  "message": "File uploaded successfully",
  "file_id": 1,
  "file_name": "receipt.pdf"
}
```

### 2. **Validate Receipt**
**POST** `/api/v1/validate`
- Validate if the uploaded file is a valid PDF.
- **Request:**
```json
{
  "file_id": 1
}
```
- **Response:**
```json
{
  "file_id": 1,
  "is_valid": true,
  "invalid_reason": null
}
```

### 3. **Process Receipt (OCR + AI Extraction)**
**POST** `/api/v1/process`
- Extracts details from the receipt using OCR and OpenAI.
- **Request:**
```json
{
  "file_id": 1
}
```
- **Response:**
```json
{
  "receipt_id": 1,
  "merchant_name": "The Venetian",
  "total_amount": 2174.62,
  "purchased_at": "2018-12-01 00:00:00",
  "raw_text": "...first 500 chars of extracted text..."
}
```

### 4. **List All Receipts**
**GET** `/api/v1/receipts`
- Returns a list of all processed receipts.
- **Response:**
```json
[
  {
    "id": 1,
    "purchased_at": "2018-12-01 00:00:00",
    "merchant_name": "The Venetian",
    "total_amount": 2174.62,
    "file_path": "uploads/venetian_434280912998.pdf",
    "created_at": "2024-07-04T12:00:00",
    "updated_at": "2024-07-04T12:00:00"
  },
  ...
]
```

### 5. **Get Receipt by ID**
**GET** `/api/v1/receipts/{id}`
- Returns details for a specific receipt.
- **Response:**
```json
{
  "id": 1,
  "purchased_at": "2018-12-01 00:00:00",
  "merchant_name": "The Venetian",
  "total_amount": 2174.62,
  "file_path": "uploads/venetian_434280912998.pdf",
  "created_at": "2024-07-04T12:00:00",
  "updated_at": "2024-07-04T12:00:00"
}
```

---

## ⚙️ Execution Instructions
- Make sure Tesseract and Poppler are installed and in your PATH.
- Set your OpenAI API key in `config.env`.
- Always initialize the database with `python -m app.utils.init_db` if you delete or reset it.
- Use the `/docs` endpoint for interactive API testing.

---

## 📝 Troubleshooting
- **Tesseract/Poppler not found:** Ensure their `bin` folders are in your system PATH.
- **OpenAI errors:** Check your API key and quota.
- **Database errors:** Re-initialize with `python -m app.utils.init_db`.
- **PDF not processing:** Make sure the file is a valid PDF and not corrupted.

---

## 📚 Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [OpenAI API](https://platform.openai.com/docs/)
- [DB Browser for SQLite](https://sqlitebrowser.org/)

---

**Happy Coding!** 