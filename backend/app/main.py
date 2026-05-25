from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import analysis
from app.api.routes import auth
from app.api.routes import doctor_visit
from app.api.routes import export
from app.api.routes import health
from app.api.routes import history
from app.api.routes import upload
from app.api.routes import vitals

from app.core.config import settings

from app.services.memory_service import (
    get_user_history
)

# =========================
# INITIALIZE FASTAPI APP
# =========================

app = FastAPI(
    title=settings.APP_NAME
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REGISTER ROUTERS
# =========================

app.include_router(health.router)

app.include_router(analysis.router)

app.include_router(upload.router)

app.include_router(export.router)

app.include_router(auth.router)

app.include_router(history.router)

# DOCTOR VISIT ROUTER
app.include_router(doctor_visit.router)

app.include_router(vitals.router)

app.include_router(vitals.analysis_router)

# =========================
# TEMP DB TEST ROUTE
# =========================

@app.get("/check-db")
async def check_db():

    data = get_user_history("demo_user")

    return data

# =========================
# MONGO TEST ROUTE
# =========================

@app.get("/mongo-test")
async def mongo_test():

    from app.core.database import get_database

    db = get_database()

    db.test.insert_one({
        "status": "working"
    })

    return {
        "message": "MongoDB working"
    }

# =========================
# FRONTEND STATIC FILES
# =========================

frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if frontend_dist.exists():

    app.mount(
        "/",
        StaticFiles(
            directory=str(frontend_dist),
            html=True
        ),
        name="frontend"
    )