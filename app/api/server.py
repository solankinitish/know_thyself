from fastapi import FastAPI
from pydantic import BaseModel
from app.services.coaching_service import CoachingService

app = FastAPI(title="KnowThyself")

service = CoachingService()

@app.get("/health")
def health():
    return {"status": "ok"}


# User Request class and post request
class UserRequest(BaseModel):
    user_id: str
    track: str

@ app.post("/user")
def register_user(request: UserRequest):
    service.get_coach(request.user_id, request.track)
    return {"status": "registered", "user_id": request.user_id, "track": request.track}


# Chat Request class and post request
class ChatRequest(BaseModel):
    user_id: str
    track: str
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = service.chat(request.user_id, request.track, request.message)
    return {"response": response}


# Data Request class and post requests
class DataRequest(BaseModel):
    user_id: str
    track: str
    data: dict

@app.post("/data/fitness")
def fitness_data(request: DataRequest):
    service.log_fitness(request.user_id, request.data)
    return {"status": "logged"}

@app.post("/data/habits")
def habits_data(request: DataRequest):
    service.log_habits(request.user_id, request.data)
    return {"status": "logged"}
