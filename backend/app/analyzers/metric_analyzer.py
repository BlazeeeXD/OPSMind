from app.models.telemetry import MetricSnapshot

class MetricAnalyzer:
    @staticmethod
    def analyze(metrics: list[MetricSnapshot]) -> list[str]:
        findings = []
        if not metrics:
            return ["No telemetry metrics found."]

        # Calculate peaks
        max_cpu = max((m.cpu for m in metrics), default=0)
        max_latency = max((m.latency for m in metrics), default=0)
        max_error_rate = max((m.error_rate for m in metrics), default=0)

        # Generate hard facts based on thresholds
        if max_cpu > 90:
            findings.append(f"Critical CPU saturation detected: Peaked at {max_cpu}%")
        elif max_cpu > 75:
            findings.append(f"Elevated CPU usage: Peaked at {max_cpu}%")

        if max_latency > 1000:
            findings.append(f"Severe latency spike detected: {max_latency}ms")
        
        if max_error_rate > 0.1:
            findings.append(f"Massive error rate increase: {(max_error_rate * 100):.1f}% of requests failed")

        return findings