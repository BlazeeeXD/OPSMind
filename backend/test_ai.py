from app.agents.investigator import InvestigatorAgent
from app.agents.remediation import RemediationAgent

# The exact output you got from Phase 3
mock_evidence = [
    "Deployment detected in service 'checkout-db' by sre-eng@company.com (Commit: a1b2c3d4) shortly before the incident.",
    "Critical CPU saturation detected: Peaked at 98.5%",
    "Severe latency spike detected: 4500.0ms",
    "Massive error rate increase: 45.0% of requests failed",
    "Frequent log (1 occurrences): 'Connection timeout acquiring database lock'",
    "Frequent log (1 occurrences): 'Query timeout for SELECT * FROM checkout_sessions'"
]

print("Running Investigator...")
investigation = InvestigatorAgent.analyze(mock_evidence)
print(investigation.model_dump_json(indent=2))

top_cause = investigation.causes[0].cause
print(f"\nTop Cause Found: {top_cause}")
print("Running Remediation...")

remediation = RemediationAgent.generate(top_cause)
print(remediation.model_dump_json(indent=2))