from sqlmodel import Session, select
from app.models.telemetry import LogEntry, MetricSnapshot, DeploymentEvent
from app.analyzers.log_analyzer import LogAnalyzer
from app.analyzers.metric_analyzer import MetricAnalyzer
from app.analyzers.deployment_analyzer import DeploymentAnalyzer

class EvidenceBuilder:
    def __init__(self, session: Session):
        self.session = session

    def build(self, incident_id: int) -> dict:
        # 1. Fetch raw data
        logs = self.session.exec(select(LogEntry).where(LogEntry.incident_id == incident_id)).all()
        metrics = self.session.exec(select(MetricSnapshot).where(MetricSnapshot.incident_id == incident_id)).all()
        deployments = self.session.exec(select(DeploymentEvent).where(DeploymentEvent.incident_id == incident_id)).all()

        # 2. Extract facts
        log_findings = LogAnalyzer.analyze(logs)
        metric_findings = MetricAnalyzer.analyze(metrics)
        deployment_findings = DeploymentAnalyzer.analyze(deployments)

        # 3. Combine into the evidence package
        all_findings = deployment_findings + metric_findings + log_findings

        return {
            "incident_id": incident_id,
            "evidence": all_findings
        }