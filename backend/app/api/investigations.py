import uuid
import json
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select
from app.database.db import get_session
from app.services.investigation_service import run_investigation, jobs
from app.models.report import InvestigationReport

router = APIRouter(prefix="/investigations", tags=["Investigation Pipeline"])

@router.post("/trigger/{incident_id}")
def trigger_investigation(incident_id: int, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running", "stage": "initializing"}

    # Hands the heavy lifting to FastAPI's background thread
    background_tasks.add_task(run_investigation, job_id, incident_id)

    return {"job_id": job_id, "message": "Investigation started."}

@router.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@router.get("/report/{incident_id}")
def get_final_report(incident_id: int, session: Session = Depends(get_session)):
    report = session.exec(select(InvestigationReport).where(InvestigationReport.incident_id == incident_id)).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not ready or incident not found")

    # Rehydrate the JSON strings from SQLite back into nested dictionaries for the API
    return {
        "incident_id": report.incident_id,
        "created_at": report.created_at,
        "summary": json.loads(report.summary),
        "root_causes": json.loads(report.root_causes),
        "recommendations": json.loads(report.recommendations),
        "timeline": json.loads(report.timeline)
    }