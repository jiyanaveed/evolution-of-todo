#!/usr/bin/env python3
"""
Simple server to run the Evolution of Todo backend
This bypasses import issues while keeping functionality intact
"""
import os
import sys
from contextlib import contextmanager

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all components with absolute imports
from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import importlib.util

# Create the app first to avoid conflicts
app = FastAPI(
    title="Evolution of Todo - Phase 2 Backend",
    version="1.0.0",
    description="A FastAPI backend for the Evolution of Todo application"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models directly from the file
models_spec = importlib.util.spec_from_file_location("models", os.path.join(os.path.dirname(__file__), "models.py"))
models_module = importlib.util.module_from_spec(models_spec)
models_spec.loader.exec_module(models_module)

# Load database directly from the file (this should be done before loading CRUD)
database_spec = importlib.util.spec_from_file_location("database", os.path.join(os.path.dirname(__file__), "database.py"))
database_module = importlib.util.module_from_spec(database_spec)
database_spec.loader.exec_module(database_module)

# Get the database functions
get_session = database_module.get_session
init_db = database_module.init_db

# Now load CRUD after database is loaded
# We need to load the CRUD functions in a way that avoids conflicts
# Let's import the functions directly by executing the code with modified imports
import models  # Import models module directly

# Create a modified version of CRUD functions that work without conflicts
def get_tasks(session: Session) -> List['models.Task']:
    """
    Retrieve all tasks from the database.
    """
    from sqlmodel import select
    from models import Task
    tasks = session.exec(select(Task)).all()
    return tasks

def get_task(session: Session, task_id: int) -> Optional['models.Task']:
    """
    Retrieve a specific task by ID from the database.
    """
    from sqlmodel import select
    from models import Task
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    return task

def create_task(session: Session, title: str) -> 'models.Task':
    """
    Create a new task in the database.
    """
    from models import Task
    task = Task(title=title, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(session: Session, task_id: int, title: str) -> Optional['models.Task']:
    """
    Update an existing task's title in the database.
    """
    task = get_task(session, task_id)
    if task:
        task.title = title
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

def delete_task(session: Session, task_id: int) -> bool:
    """
    Delete a task from the database by ID.
    """
    task = get_task(session, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False

def toggle_task_completion(session: Session, task_id: int) -> Optional['models.Task']:
    """
    Toggle the completion status of a task in the database.
    """
    task = get_task(session, task_id)
    if task:
        task.completed = not task.completed
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

# Get the response models
TaskResponse = models_module.TaskResponse
TaskCreate = models_module.TaskCreate
TaskUpdate = models_module.TaskUpdate

@app.on_event("startup")
def on_startup():
    """
    Initialize the database on application startup.
    """
    init_db()

@app.get("/tasks", response_model=List[TaskResponse])
def read_tasks(session: Session = Depends(get_session)):
    """
    Retrieve all tasks from the database.
    """
    tasks = get_tasks(session)
    return tasks

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task_endpoint(task_create: TaskCreate, session: Session = Depends(get_session)):
    """
    Create a new task in the database.
    """
    task = create_task(session, title=task_create.title)
    return task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a specific task by ID from the database.
    """
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    """
    Update an existing task's title in the database.
    """
    task = update_task(session, task_id, title=task_update.title)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    """
    Delete a task from the database by ID.
    """
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return  # Return empty response for 204 status

@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion_endpoint(task_id: int, session: Session = Depends(get_session)):
    """
    Toggle the completion status of a task in the database.
    """
    task = toggle_task_completion(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Evolution of Todo - Phase 2 Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description='Run the Evolution of Todo backend')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    parser.add_argument('--host', type=str, default="127.0.0.1", help='Host to run the server on (default: 127.0.0.1)')
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)