# backend/app/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from typing import List
import logging
from .utils import validate_file, load_job_configs, load_config

# Initialize FastAPI app
app = FastAPI(title="Resume Parser API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def read_root():
    """Root endpoint to check API status."""
    return {"status": "OK", "message": "Resume Parser API is running"}

@app.get("/config")
async def get_config():
    """Endpoint to retrieve current configuration."""
    return load_config()

@app.get("/jobs")
async def get_jobs():
    """Endpoint to retrieve available job configurations."""
    return load_job_configs()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a resume file.
    
    Args:
        file (UploadFile): The resume file to be processed
    
    Returns:
        dict: Processed resume data
    """
    try:
        # Get file extension
        file_extension = Path(file.filename).suffix
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file
        validate_file(file_size, file_extension)
        
        # Save file
        file_path = UPLOAD_DIR / f"{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Successfully uploaded file: {file.filename}")
        
        # Here you would typically add code to process the resume
        # For now, we'll just return a success message
        return {
            "filename": file.filename,
            "size": file_size,
            "status": "uploaded",
            "message": "File successfully uploaded and pending processing"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
    finally:
        await file.close()

@app.delete("/upload/{filename}")
async def delete_file(filename: str):
    """
    Delete an uploaded file.
    
    Args:
        filename (str): Name of the file to delete
    
    Returns:
        dict: Deletion status
    """
    try:
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        os.remove(file_path)
        logger.info(f"Successfully deleted file: {filename}")
        
        return {
            "status": "success",
            "message": f"File {filename} successfully deleted"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting file: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)