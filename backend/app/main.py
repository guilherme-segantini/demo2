"""FastAPI application entry point for CodeScale Research Radar."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database import init_db
from app.api.radar import router as radar_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="CodeScale Research Radar",
    description="Signal vs Noise classification API for architectural decision support",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(radar_router)


@app.get("/")
def root():
    """Root endpoint with API info."""
    return {
        "name": "CodeScale Research Radar API",
        "version": "1.0.0",
        "docs": "/docs",
    }
