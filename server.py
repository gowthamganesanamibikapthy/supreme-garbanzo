import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime
import sqlite3

app = FastAPI(title="AURA Companion Cloud Engine", version="1.0.0")

def init_db():
    conn = sqlite3.connect("aura_cloud_fallback.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cloud_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            status TEXT DEFAULT 'ACTIVE',
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            val TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO system_config (key, val) VALUES ('active_skin', 'CYBER_HUD')")
    conn.commit()
    conn.close()

init_db()

class TaskSchema(BaseModel):
    task_text: str

class TaskResponse(BaseModel):
    task_text: str
    status: str

class SkinSchema(BaseModel):
    skin_name: str

@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_active_tasks():
    conn = sqlite3.connect("aura_cloud_fallback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task_text, status FROM cloud_tasks WHERE status = 'ACTIVE'")
    tasks = [{"task_text": row[0], "status": row[1]} for row in cursor.fetchall()]
    conn.close()
    return tasks

@app.post("/api/tasks", response_model=TaskResponse)
async def create_new_task(task: TaskSchema):
    conn = sqlite3.connect("aura_cloud_fallback.db")
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO cloud_tasks (task_text, created_at) VALUES (?, ?)", (task.task_text, now))
    conn.commit()
    conn.close()
    return {"task_text": task.task_text, "status": "ACTIVE"}

@app.post("/api/tasks/complete")
async def mark_task_resolved(task: TaskSchema):
    conn = sqlite3.connect("aura_cloud_fallback.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE cloud_tasks SET status = 'COMPLETED' WHERE task_text = ?", (task.task_text,))
    conn.commit()
    conn.close()
    return {"message": "Success"}

@app.get("/api/config/skin", response_model=SkinSchema)
async def get_current_skin():
    conn = sqlite3.connect("aura_cloud_fallback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT val FROM system_config WHERE key = 'active_skin'")
    skin = cursor.fetchone()
    conn.close()
    return {"skin_name": skin[0] if skin else "CYBER_HUD"}

@app.post("/api/config/skin")
async def update_active_skin(skin: SkinSchema):
    if skin.skin_name not in ["CYBER_HUD", "KAWAII_PET", "ZEN_OASIS"]:
        raise HTTPException(status_code=400, detail="Invalid target configuration.")
    conn = sqlite3.connect("aura_cloud_fallback.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE system_config SET val = ? WHERE key = 'active_skin'", (skin.skin_name,))
    conn.commit()
    conn.close()
    return {"message": "Skin matrix shifted configuration."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
