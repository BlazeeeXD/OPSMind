from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- Add this import
from sqlmodel import SQLModel

from app.models.incident import Incident
from app.models.telemetry import LogEntry, MetricSnapshot, DeploymentEvent
from app.models.report import InvestigationReport

from app.database.db import engine
from app.api import incidents, ingestion, demo, investigations

app = FastAPI(title="Incident Intelligence API")

# ---> ADD THIS CORS BLOCK <---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your React app on any port to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(incidents.router)
app.include_router(ingestion.router)
app.include_router(demo.router)
app.include_router(investigations.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}