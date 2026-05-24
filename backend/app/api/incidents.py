from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.incident import Incident
from app.schemas.requests import IncidentCreate

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.post("/")
def create_incident(incident: IncidentCreate, session: Session = Depends(get_session)):
    db_incident = Incident(**incident.model_dump())
    session.add(db_incident)
    session.commit()
    session.refresh(db_incident)
    return db_incident

# ---> ADD THIS NEW ROUTE <---
@router.get("/")
def list_incidents(session: Session = Depends(get_session)):
    # Fetch all incidents, newest first
    incidents = session.exec(select(Incident).order_by(Incident.id.desc())).all()
    return incidents

@router.get("/{incident_id}")
def get_incident(incident_id: int, session: Session = Depends(get_session)):
    incident = session.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident