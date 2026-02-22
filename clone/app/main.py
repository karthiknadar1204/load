"""
FastAPI server for parse and export.

Run from repo root (clone):
  PYTHONPATH=src uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Or after: pip install -e .
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import documents, export, health

app = FastAPI(
    title="Unstructured Parse & Export API",
    description="Parse PDFs and export to Markdown, HTML, or Excel.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"service": "unstructured-api", "docs": "/docs", "health": "/api/v1/health"}
