"""FastAPI entry point: app setup, CORS, DB lifespan."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database.db import init_db, close_db
from .routers import cook, weather, equipment, report
from .models.schemas import HealthResponse
from .services.logging_service import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    setup_logging()
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="The Predictive Pitmaster",
    description="BBQ cook time prediction using physics simulation + Monte Carlo",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(cook.router)
app.include_router(weather.router)
app.include_router(equipment.router)
app.include_router(report.router)


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", version="1.0.0")
