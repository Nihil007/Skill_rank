# Import FastAPI class
from fastapi import FastAPI
# Import router from health.py
from health import router as health_router
# Import logging setup function
from logging_config import setup_logging
# Import router from students.py
from students import router as students_router
# Import router from auth_routes.py
from auth_routes import authRouter

from fastapi.middleware.cors import CORSMiddleware

# Instance of the FastAPI app
app = FastAPI(title="FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the authentiction router
app.include_router(authRouter)

# Register the students router
app.include_router(students_router)

# Set up logging configuration
setup_logging()

# Register the health check router
app.include_router(health_router)

# Root endpoint to confirm app is running
@app.get("/")
def root():
    # Returns a welcome message to confirm the app is running
    return {"message": "Welcome to the FastAPI app"}
