import uvicorn
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError as e:
    raise ImportError("FastAPI and Pydantic are required. Install with: pip install fastapi pydantic uvicorn") from e
from typing import List

# Structural relative imports from local component siblings
from database import CloudDatabase
from auth_service import AuthenticationService
from task_service import TaskService

app = FastAPI(title="AURA Production Component Cloud Framework", version="1.2.0")

# Instantiate Singleton Microservice Component Engines
db_manager = CloudDatabase()
auth_service = AuthenticationService(db_manager)
task_service = TaskService(db_manager)

# --- Shared Data Schema Payloads ---
class UserAuthSchema(BaseModel):
    username: str
    password: str

class TaskSchema(BaseModel):
    username: str
    task_text: str

class SkinSchema(BaseModel):
    username: str
    skin_name: str

# --- API Route Mapping Interfacings ---
@app.post("/api/auth/register")
async def register(user: UserAuthSchema):
    if not auth_service.process_registration(user.username, user.password):
        raise HTTPException(status_code=400, detail="Account duplicate profile mismatch.")
    return {"message": "Registration successful."}

@app.post("/api/auth/login")
async def login(user: UserAuthSchema):
    if not auth_service.verify_login(user.username, user.password):
        raise HTTPException(status_code=401, detail="Invalid security credentials.")
    return {"message": "Authenticated.", "username": user.username}

@app.post("/api/tasks/fetch")
async def get_tasks(user: SkinSchema):
    return task_service.fetch_user_tasks(user.username)

@app.post("/api/tasks")
async def add_task(task: TaskSchema):
    return task_service.add_user_task(task.username, task.task_text)

@app.post("/api/tasks/complete")
async def finish_task(task: TaskSchema):
    return task_service.complete_user_task(task.username, task.task_text)

@app.post("/api/config/get-skin")
async def get_skin(user: SkinSchema):
    return task_service.get_skin_config(user.username)

@app.post("/api/config/skin")
async def change_skin(skin: SkinSchema):
    if skin.skin_name not in ["CYBER_HUD", "KAWAII_PET", "ZEN_OASIS"]:
        raise HTTPException(status_code=400, detail="Invalid skin design identifier.")
    return task_service.update_skin_config(skin.username, skin.skin_name)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
