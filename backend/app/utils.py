# backend/app/utils.py
import os
import json
from typing import Dict, Any
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    return {
        'MAX_FILE_SIZE': int(os.getenv('MAX_FILE_SIZE', 5 * 1024 * 1024)),  # 5MB default
        'ALLOWED_EXTENSIONS': set(os.getenv('ALLOWED_EXTENSIONS', '.pdf').split(',')),
        'MODEL_PATH': os.getenv('MODEL_PATH', 'bert-base-uncased')
    }

def load_job_configs() -> Dict[str, Any]:
    """Load job configurations from JSON file."""
    try:
        with open("job_configs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("job_configs.json not found")
        raise HTTPException(
            status_code=500,
            detail="Job configurations not found"
        )
    except json.JSONDecodeError:
        logger.error("Error parsing job_configs.json")
        raise HTTPException(
            status_code=500,
            detail="Error parsing job configurations"
        )

def validate_file(file_size: int, file_extension: str) -> None:
    """Validate uploaded file size and extension."""
    config = load_config()
    
    if file_size > config['MAX_FILE_SIZE']:
        logger.warning(f"File size {file_size} exceeds maximum allowed size {config['MAX_FILE_SIZE']}")
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {config['MAX_FILE_SIZE'] // (1024 * 1024)}MB"
        )
    
    if file_extension.lower() not in config['ALLOWED_EXTENSIONS']:
        logger.warning(f"Invalid file extension: {file_extension}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed extensions: {', '.join(config['ALLOWED_EXTENSIONS'])}"
        )