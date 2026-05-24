import os
import google.generativeai as genai
from app.schemas.responses import RemediationPlan
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class RemediationAgent:
    @staticmethod
    def generate(primary_cause: str) -> RemediationPlan:
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"""
        You are a Senior Site Reliability Engineer. 
        A production incident is currently ongoing. The primary root cause has been identified as:
        "{primary_cause}"
        
        Provide a safe, effective remediation plan to mitigate this issue.
        
        You must return a valid JSON object strictly matching this schema:
        {{
          "actions": ["Step 1", "Step 2", "Step 3"],
          "recovery_time": "string (e.g., '5-10 minutes')",
          "impact": "string (What happens when we run these actions?)",
          "risk": "string (Low/Medium/High and why)"
        }}
        """
        
        response = model.generate_content(prompt)
        
        return RemediationPlan.model_validate_json(response.text)