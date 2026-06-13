from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI(title="Mini Incident Tracker API")


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str
    
class IncidentStatusUpdate(BaseModel):
        status: str

class Incident(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str


incidents: List[Incident] = []


@app.get("/")
def health_check():
    return {"status": "OK", "message": "Mini Incident Tracker API is running."}


@app.post("/incidents", response_model=Incident)
def create_incident(incident_data: IncidentCreate):
    allowed_severities = ["low", "medium", "high", "critical"]

    if incident_data.severity not in allowed_severities:
        raise HTTPException(
            status_code=400,
            detail="Invalid severity. Allowed values are: low, medium, high, critical",
        )

    new_incident = Incident(
        id=len(incidents) + 1,
        title=incident_data.title,
        description=incident_data.description,
        severity=incident_data.severity,
        status="open",
    )

    incidents.append(new_incident)

    return new_incident

@app.get("/incidents", response_model=List[Incident])
def get_incidents():
    return incidents

@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: int):
    for incident in incidents:
        if incident.id == incident_id:
            return incident

    raise HTTPException(status_code=404, detail="Incident not found")

@app.patch("/incidents/{incident_id}/status", response_model=Incident)
def update_incident_status(incident_id: int, status_data: IncidentStatusUpdate):
    allowed_statuses = ["open", "investigating", "resolved", "closed"]

    if status_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Allowed values are: open, investigating, resolved, closed",
        )

    for incident in incidents:
        if incident.id == incident_id:
            incident.status = status_data.status
            return incident

    raise HTTPException(status_code=404, detail="Incident not found")