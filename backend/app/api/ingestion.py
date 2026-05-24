from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.db import get_session
from app.models.telemetry import LogEntry, MetricSnapshot, DeploymentEvent
from app.schemas.requests import LogCreate, MetricCreate, DeploymentCreate

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/logs")
def ingest_log(log_in: LogCreate, session: Session = Depends(get_session)):
    db_log = LogEntry(**log_in.model_dump())
    session.add(db_log)
    session.commit()
    return {"status": "success", "id": db_log.id}

@router.post("/metrics")
def ingest_metric(metric_in: MetricCreate, session: Session = Depends(get_session)):
    db_metric = MetricSnapshot(**metric_in.model_dump())
    session.add(db_metric)
    session.commit()
    return {"status": "success", "id": db_metric.id}

@router.post("/deployments")
def ingest_deployment(deployment_in: DeploymentCreate, session: Session = Depends(get_session)):
    db_deployment = DeploymentEvent(**deployment_in.model_dump())
    session.add(db_deployment)
    session.commit()
    return {"status": "success", "id": db_deployment.id}