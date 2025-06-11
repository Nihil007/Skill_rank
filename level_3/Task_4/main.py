# Import FastAPI class
from fastapi import FastAPI
# Import router from health.py
from health import router as health_router
# Import logging setup function
from logging_config import setup_logging

# Set up logging configuration
setup_logging()

# Instance of the FastAPI app
app = FastAPI(title="FastAPI Health Check")

# Register the health check router
app.include_router(health_router)

# Root endpoint to confirm app is running
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI app"}
