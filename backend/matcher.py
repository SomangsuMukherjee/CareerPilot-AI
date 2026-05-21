import re
from collections import Counter

DEVOPS_SKILLS = [
    "python", "fastapi", "docker", "kubernetes", "terraform", "linux",
    "aws", "azure", "git", "github actions", "ci/cd", "postgresql",
    "prometheus", "grafana", "redis", "bash", "ansible", "jenkins",
    "rest api", "nginx", "cloud", "devops", "monitoring"
]

AI_SKILLS = [
    "ai", "machine learning", "llm", "large language model",
    "prompt engineering", "automation", "openai", "rag"
]

def clean_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9+#./ -]", " ", text.lower())

def extract_skills(text: str):
    cleaned = clean_text(text)
    found = []

    for skill in DEVOPS_SKILLS + AI_SKILLS:
        if skill in cleaned:
            found.append(skill)

    return sorted(set(found))

def calculate_match(cv_text: str, job_text: str):
    cv_skills = extract_skills(cv_text)
    job_skills = extract_skills(job_text)

    matched = sorted(set(cv_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(cv_skills))

    if not job_skills:
        score = 0
    else:
        score = round((len(matched) / len(job_skills)) * 100)

    recruiter_summary = generate_recruiter_summary(score, matched, missing)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "cv_detected_skills": cv_skills,
        "job_detected_skills": job_skills,
        "recruiter_summary": recruiter_summary
    }

def generate_recruiter_summary(score, matched, missing):
    if score >= 80:
        level = "Strong match"
    elif score >= 60:
        level = "Good partial match"
    elif score >= 40:
        level = "Moderate match"
    else:
        level = "Weak match"

    return {
        "verdict": level,
        "summary": f"The candidate matches {score}% of the detected job requirements.",
        "strengths": matched[:8],
        "improvement_areas": missing[:8],
        "recommendation": "Tailor the CV by emphasizing matched skills and adding evidence for missing high-value keywords."
    }