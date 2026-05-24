from sqlmodel import Session, select
from app.models.telemetry import LogEntry, DeploymentEvent

class TimelineBuilder:
    @staticmethod
    def build(session: Session, incident_id: int) -> list[dict]:
        # Fetch deployments and logs for this incident
        logs = session.exec(select(LogEntry).where(LogEntry.incident_id == incident_id)).all()
        deployments = session.exec(select(DeploymentEvent).where(DeploymentEvent.incident_id == incident_id)).all()

        events = []
        
        # Add deployments to timeline
        for dep in deployments:
            events.append({
                "time": dep.deployment_time, 
                "event": f"Deployment: Commit {dep.commit_hash} pushed to {dep.service} by {dep.author}"
            })

        # Add only high-severity logs to timeline to reduce noise
        for log in logs:
            if log.level in ["WARNING", "ERROR", "CRITICAL"]:
                events.append({
                    "time": log.timestamp, 
                    "event": f"{log.level}: {log.message}"
                })

        # Sort chronologically
        events.sort(key=lambda x: x["time"])

        # Format timestamps for a clean JSON output
        return [{"time": e["time"].strftime("%H:%M:%S"), "event": e["event"]} for e in events]