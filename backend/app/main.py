from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import analysis
from app.api.routes import auth
from app.api.routes import export
from app.api.routes import health
from app.api.routes import history
from app.api.routes import upload
from app.api.routes import vitals

from app.core.config import settings


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME
)


# Register routers
app.include_router(health.router)
app.include_router(analysis.router)
app.include_router(upload.router)
app.include_router(export.router)
app.include_router(auth.router)
app.include_router(history.router)
app.include_router(vitals.router)


frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")