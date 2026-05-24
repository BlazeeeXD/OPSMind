from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class InvestigationReport(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    incident_id: int = Field(unique=True)
    summary: str # Stored as JSON string
    root_causes: str # Stored as JSON string
    recommendations: str # Stored as JSON string
    timeline: str # Stored as JSON string
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))