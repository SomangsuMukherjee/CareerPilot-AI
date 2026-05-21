from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from matcher import calculate_match

app = FastAPI(
    title="CareerPilot AI",
    description="AI-powered job search intelligence platform for CV matching, skill gap analysis, and application tracking.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

applications = []


class MatchRequest(BaseModel):
    cv_text: str
    job_description: str


class ApplicationRequest(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    job_url: str | None = None
    notes: str | None = None


@app.get("/")
def root():
    return {
        "project": "CareerPilot AI",
        "status": "running",
        "message": "AI-powered job search intelligence platform"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/match")
def match_cv_to_job(request: MatchRequest):
    return calculate_match(request.cv_text, request.job_description)


@app.post("/applications")
def add_application(request: ApplicationRequest):
    application = {
        "id": len(applications) + 1,
        "company": request.company,
        "role": request.role,
        "status": request.status,
        "job_url": request.job_url,
        "notes": request.notes,
        "created_at": datetime.utcnow().isoformat()
    }
    applications.append(application)
    return application


@app.get("/applications")
def get_applications():
    return {
        "count": len(applications),
        "applications": applications
    }


@app.put("/applications/{app_id}")
def update_application(app_id: int, request: ApplicationRequest):
    for app_item in applications:
        if app_item["id"] == app_id:
            app_item["company"] = request.company
            app_item["role"] = request.role
            app_item["status"] = request.status
            app_item["job_url"] = request.job_url
            app_item["notes"] = request.notes
            return app_item

    return {"error": "Application not found"}


@app.delete("/applications/{app_id}")
def delete_application(app_id: int):
    global applications

    applications = [
        app_item for app_item in applications
        if app_item["id"] != app_id
    ]

    return {"message": "Application deleted"}


@app.get("/analytics")
def analytics():
    total = len(applications)
    statuses = {}

    for app_item in applications:
        status = app_item["status"]
        statuses[status] = statuses.get(status, 0) + 1

    return {
        "total_applications": total,
        "status_breakdown": statuses
    }