from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.auth_routes import router as auth_router
from app.api.routes import router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(
    title="PDF RAG Assistant",
    description="Upload PDFs and ask questions answered strictly from their content, with page-level citations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Creates the users table (SQLite file) on first run; a no-op afterwards.
    init_db()


# All API endpoints live under /api (health, documents, upload, ask, reset,
# and auth: /api/auth/signup, /api/auth/login, /api/auth/me)
app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api")

# Serve the vanilla JS frontend from this same service, so a single Render
# web service hosts both the API and the UI (frontend/script.js calls /api/*,
# which is same-origin here, so no CORS issues in production).
#
# backend/app/main.py -> app -> backend -> repo root -> frontend
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
