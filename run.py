import uvicorn
from frontend.app import app as frontend_app
from daas_api import app as api_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create main application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount both apps
app.mount("/api", api_app)
app.mount("/", frontend_app)

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload
    )
