# app/core/middleware.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def setup_cors(app: FastAPI):
    """
    Configure CORS for the FastAPI app.
    """
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[
        #     "http://localhost:3000",   # frontend URL(s)
        #     "https://yourdomain.com"   # production URL
        # ],
        allow_origins=["*"],  # Allows all origins"],
        allow_credentials=True,
        allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
        allow_headers=["*"],
    )
