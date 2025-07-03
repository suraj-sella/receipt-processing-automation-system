"""
Main FastAPI application for Receipt Processing System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
from app.api.routes import router

# Load environment variables
load_dotenv("config.env")

# Create FastAPI application
app = FastAPI(
    title="Receipt Processing API",
    description="API for processing scanned receipts using OCR and AI",
    version="1.0.0"
)

# Add CORS middleware (allows web browsers to access our API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you'd specify actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

# Simple health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Receipt Processing API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# This runs the application when you execute this file directly
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    ) 