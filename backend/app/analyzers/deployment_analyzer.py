from app.models.telemetry import DeploymentEvent

class DeploymentAnalyzer:
    @staticmethod
    def analyze(deployments: list[DeploymentEvent]) -> list[str]:
        findings = []
        if not deployments:
            return [] # Empty list is fine, means no deployment caused it
        
        for dep in deployments:
            findings.append(f"Deployment detected in service '{dep.service}' by {dep.author} (Commit: {dep.commit_hash}) shortly before the incident.")

        return findings