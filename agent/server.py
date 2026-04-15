import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_it_task

app = FastAPI(
    title="IT-Agent API",
    description="AI agent that completes IT support tasks by navigating a browser like a human. No DOM shortcuts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class TaskRequest(BaseModel):
    task: str


class TaskResponse(BaseModel):
    status: str
    result: str
    task: str
    duration_seconds: int = 0


@app.get("/health")
async def health():
    return {"status": "ok", "agent": "ready", "version": "1.0.0"}


@app.post("/run-task", response_model=TaskResponse)
async def run_task(request: TaskRequest):
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    result = await run_it_task(request.task)
    return TaskResponse(**result)


@app.get("/examples")
async def examples():
    return {
        "tasks": [
            "Reset password for john@company.com",
            "Create a new user named Alex Kim with email alex@company.com and role Developer",
            "Assign license L005 to emma@company.com",
            "Deactivate the account for mike@company.com",
            "Check if newuser@company.com exists — if not, create them with name New User and role Analyst, then assign license L006"
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
