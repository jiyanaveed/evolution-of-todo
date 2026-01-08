#!/usr/bin/env python3
"""
Simple server to run the Evolution of Todo backend with SQLite support
"""
import os
import sys
from contextlib import contextmanager

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import SQLModel, create_engine, Session, Field
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import ConfigDict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the app first to avoid conflicts
app = FastAPI(
    title="Evolution of Todo - Phase 2 Backend",
    version="1.0.0",
    description="A FastAPI backend for the Evolution of Todo application"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models directly in this file to avoid conflicts
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False

# Request models for API
class TaskCreate(SQLModel):
    title: str

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(SQLModel):
    id: int
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)

# Use SQLite database
DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize the database by creating all tables."""
    SQLModel.metadata.create_all(engine)

def get_tasks(session: Session) -> List[Task]:
    """Retrieve all tasks from the database."""
    from sqlmodel import select
    tasks = session.exec(select(Task)).all()
    return tasks

def get_task(session: Session, task_id: int) -> Optional[Task]:
    """Retrieve a specific task by ID from the database."""
    from sqlmodel import select
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    return task

def create_task(session: Session, title: str) -> Task:
    """Create a new task in the database."""
    task = Task(title=title, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(session: Session, task_id: int, title: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
    """Update an existing task's title and/or completion status in the database."""
    task = get_task(session, task_id)
    if task:
        if title is not None:
            task.title = title
        if completed is not None:
            task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task from the database by ID."""
    task = get_task(session, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False

def toggle_task_completion(session: Session, task_id: int) -> Optional[Task]:
    """Toggle the completion status of a task in the database."""
    task = get_task(session, task_id)
    if task:
        task.completed = not task.completed
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

@app.on_event("startup")
def on_startup():
    """Initialize the database on application startup."""
    init_db()

@app.get("/tasks", response_model=List[TaskResponse])
def read_tasks(session: Session = Depends(get_session)):
    """Retrieve all tasks from the database."""
    logger.info("Getting all tasks")
    from sqlmodel import select
    tasks = session.exec(select(Task)).all()
    return tasks

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task_endpoint(task_create: TaskCreate, session: Session = Depends(get_session)):
    """Create a new task in the database."""
    logger.info(f"Creating task with title: {task_create.title}")
    task = create_task(session, title=task_create.title)
    return task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, session: Session = Depends(get_session)):
    """Retrieve a specific task by ID from the database."""
    logger.info(f"Getting task with ID: {task_id}")
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    """Update an existing task's title and/or completion status in the database."""
    logger.info(f"Updating task {task_id} with title: {task_update.title}, completed: {task_update.completed}")
    task = update_task(session, task_id, title=task_update.title, completed=task_update.completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    """Delete a task from the database by ID."""
    logger.info(f"Deleting task with ID: {task_id}")
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return  # Return empty response for 204 status

@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion_endpoint(task_id: int, session: Session = Depends(get_session)):
    """Toggle the completion status of a task in the database."""
    logger.info(f"Toggling completion for task with ID: {task_id}")
    task = toggle_task_completion(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Evolution of Todo - Phase 2 Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description='Run the Evolution of Todo backend')
    parser.add_argument('--port', type=int, default=8001, help='Port to run the server on (default: 8001)')
    parser.add_argument('--host', type=str, default="127.0.0.1", help='Host to run the server on (default: 127.0.0.1)')
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)