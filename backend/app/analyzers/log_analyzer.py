from collections import Counter
from app.models.telemetry import LogEntry

class LogAnalyzer:
    @staticmethod
    def analyze(logs: list[LogEntry]) -> list[str]:
        findings = []
        if not logs:
            return ["No logs found for this incident."]

        # Filter for high-severity logs
        error_logs = [log for log in logs if log.level in ["WARNING", "ERROR", "CRITICAL"]]
        
        if error_logs:
            findings.append(f"System generated {len(error_logs)} high-severity logs (WARNING/ERROR/CRITICAL).")
            
            # Find the most repeated error messages
            messages = [log.message for log in error_logs]
            counter = Counter(messages)
            most_common = counter.most_common(3)
            
            for msg, count in most_common:
                findings.append(f"Frequent log ({count} occurrences): '{msg}'")

        return findings