from pydantic import BaseModel, Field

class RootCause(BaseModel):
    cause: str
    confidence: int = Field(ge=0, le=100)
    reasoning: str

class InvestigationResult(BaseModel):
    causes: list[RootCause]

class RemediationPlan(BaseModel):
    actions: list[str]
    recovery_time: str
    impact: str
    risk: str