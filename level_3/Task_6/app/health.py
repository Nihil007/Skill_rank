# Import FastAPI's router class
from fastapi import APIRouter 
# Import the standard logging module
import logging  

# Create an API router instance
router = APIRouter()

# Create a logger for this module
logger = logging.getLogger(__name__)

# Define the health check endpoint
@router.get("/api/healthz")
def health_check():
    try:
        # Log the incoming health check request
        logger.info("Health check endpoint called.")
        
        # Return a healthy status response
        return {"status": "OK"}
    
    except Exception as e:
        # Log any error
        logger.error(f"Health check error: {e}")
        
        # Return error response
        return {"status": "ERROR", "detail": str(e)}
