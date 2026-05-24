import json
from sqlmodel import Session
from app.database.db import engine
from app.models.incident import Incident
from app.models.report import InvestigationReport

from app.builders.evidence_builder import EvidenceBuilder
from app.agents.investigator import InvestigatorAgent
from app.agents.remediation import RemediationAgent
from app.builders.timeline_builder import TimelineBuilder

# In-memory dictionary to track job state instantly (Perfect for Hackathons)
jobs = {}

def run_investigation(job_id: str, incident_id: int):
    # Create a fresh session for the background thread
    with Session(engine) as session:
        try:
            # Stage 1: Evidence Extraction
            jobs[job_id]["stage"] = "extracting_evidence"
            evidence_data = EvidenceBuilder(session).build(incident_id)
            facts = evidence_data["evidence"]

            # Stage 2: Root Cause Analysis
            jobs[job_id]["stage"] = "analyzing_root_cause"
            investigation = InvestigatorAgent.analyze(facts)
            top_cause = investigation.causes[0].cause

            # Stage 3: Remediation Plan
            jobs[job_id]["stage"] = "generating_remediation"
            remediation = RemediationAgent.generate(top_cause)

            # Stage 4: Timeline Generation
            jobs[job_id]["stage"] = "building_timeline"
            timeline = TimelineBuilder.build(session, incident_id)

            # Stage 5: Final Report Assembly
            jobs[job_id]["stage"] = "finalizing_report"
            
            incident = session.get(Incident, incident_id)
            incident.status = "resolved" # Mark incident as handled

            # ---> ADD THIS BLOCK TO FIX THE ERROR <---
            from sqlmodel import select
            existing_report = session.exec(select(InvestigationReport).where(InvestigationReport.incident_id == incident_id)).first()
            if existing_report:
                session.delete(existing_report)
                session.commit()
            # -----------------------------------------

            report = InvestigationReport(
                incident_id=incident_id,
                summary=json.dumps({
                    "title": incident.title, 
                    "severity": incident.severity, 
                    "affected_service": incident.affected_service
                }),
                root_causes=investigation.model_dump_json(),
                recommendations=remediation.model_dump_json(),
                timeline=json.dumps(timeline)
            )

            # Save everything to SQLite
            session.add(report)
            session.add(incident)
            session.commit()

            # Job Finished
            jobs[job_id]["stage"] = "completed"
            jobs[job_id]["status"] = "success"

        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)