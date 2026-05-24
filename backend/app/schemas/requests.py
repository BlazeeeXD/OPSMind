from pydantic import BaseModel

class IncidentCreate(BaseModel):
    title: str
    severity: str
    affected_service: str

class LogCreate(BaseModel):
    incident_id: int
    service: str
    level: str
    message: str

class MetricCreate(BaseModel):
    incident_id: int
    cpu: float
    memory: float
    latency: float
    error_rate: float
    request_count: int

class DeploymentCreate(BaseModel):
    incident_id: int
    service: str
    commit_hash: str
    author: str