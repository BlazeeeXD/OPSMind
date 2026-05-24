from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class LogEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    incident_id: int = Field(index=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    service: str
    level: str
    message: str

class MetricSnapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    incident_id: int = Field(index=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    cpu: float
    memory: float
    latency: float
    error_rate: float
    request_count: int

class DeploymentEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    incident_id: int = Field(index=True)
    service: str
    commit_hash: str
    author: str
    deployment_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))