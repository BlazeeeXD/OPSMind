import os
import json
import google.generativeai as genai
from app.schemas.responses import InvestigationResult
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class InvestigatorAgent:
    @staticmethod
    def analyze(evidence: list[str]) -> InvestigationResult:
        # Using gemini-1.5-flash because it's blazing fast and perfect for JSON
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"""
        You are a Senior Site Reliability Engineer analyzing a production incident.
        Analyze the following extracted evidence facts and identify the likely root causes.
        Rank them by confidence (0-100). Explain your reasoning clearly and concisely.
        
        EVIDENCE FACTS:
        {json.dumps(evidence, indent=2)}
        
        You must return a valid JSON object strictly matching this schema:
        {{
          "causes": [
            {{
              "cause": "Short title of the root cause",
              "confidence": integer between 0 and 100,
              "reasoning": "Brief explanation mapping evidence to this cause"
            }}
          ]
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Pydantic strictly validates the LLM's JSON string
        return InvestigationResult.model_validate_json(response.text)