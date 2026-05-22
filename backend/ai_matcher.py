import os
import json
import requests


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def analyze_with_ai(cv_text: str, job_description: str):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "error": "GROQ_API_KEY is not configured on the server."
        }

    prompt = f"""
You are an experienced technical recruiter and career advisor.

Analyze the CV against the job description.

Return ONLY valid JSON. No markdown. No explanation outside JSON.

JSON schema:
{{
  "match_score": number,
  "verdict": string,
  "matched_skills": [string],
  "missing_skills": [string],
  "strengths": [string],
  "weaknesses": [string],
  "recruiter_summary": string,
  "cv_improvements": [string],
  "tailored_bullets": [string]
}}

Rules:
- match_score must be 0 to 100.
- Be realistic, not overly generous.
- Detect skills dynamically from both texts.
- Focus on technical fit, DevOps/cloud/backend/AI relevance, experience level, and keyword alignment.
- If something is missing, say clearly.
- tailored_bullets should rewrite or suggest CV bullet points for this specific job.

CV:
{cv_text}

JOB DESCRIPTION:
{job_description}
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a strict technical recruiter. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        return {
            "error": "AI analysis failed",
            "details": response.text
        }

    content = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_response": content
        }