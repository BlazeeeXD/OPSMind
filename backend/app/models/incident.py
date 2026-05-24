from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Incident(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    severity: str
    status: str = Field(default="investigating")
    affected_service: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))