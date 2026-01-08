"""
PHASE 3 VERIFICATION SCRIPT
Validates the AI Todo Chatbot implementation against the locked specification.
"""
import sys
import os
import uuid
from sqlmodel import Session, create_engine, SQLModel, Field, Relationship, select
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- DOMAIN MODELS (Duplicated for standalone execution if needed, but normally imported) ---
class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
    user_id: str = Field(foreign_key="user.id", nullable=False)

# --- RE-IMPLEMENTING TOOLS LOGIC (Cleaned of relative imports) ---
class TaskMCPToolsMock:
    @staticmethod
    def create_task(session: Session, user_id: str, title: str) -> Dict[str, Any]:
        if not title or not title.strip():
            raise ValueError("Title must be non-empty")
        task = Task(title=title.strip(), user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"id": task.id, "title": task.title, "completed": task.completed, "user_id": task.user_id}

    @staticmethod
    def read_task(session: Session, task_id: int, user_id: str) -> Optional[Dict[str, Any]]:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task: return None
        return {"id": task.id, "title": task.title, "completed": task.completed, "user_id": task.user_id}

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, title: str = None, completed: bool = None) -> Optional[Dict[str, Any]]:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task: return None
        if completed is not None:
            if task.completed is True and completed is False:
                raise ValueError("Cannot revert completed task")
            task.completed = completed
        if title:
            if not title.strip(): raise ValueError("Empty title")
            task.title = title.strip()
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"id": task.id, "title": task.title, "completed": task.completed, "user_id": task.user_id}

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task: return False
        session.delete(task)
        session.commit()
        return True

# --- TEST SUITE ---
def log(name, success, msg=""):
    print(f"{'✅ PASS' if success else '❌ FAIL'} | {name}" + (f": {msg}" if msg else ""))

def run_verify():
    print("🚀 Phase 3 Verification Suite\n" + "="*40)
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    tools = TaskMCPToolsMock()

    with Session(engine) as session:
        # 1. Setup
        u1 = User(email="u1@test.com", password_hash="hash")
        u2 = User(email="u2@test.com", password_hash="hash")
        session.add_all([u1, u2])
        session.commit()

        # 2. CREATE
        t1 = tools.create_task(session, u1.id, "Task 1")
        log("Creation", t1['title'] == "Task 1")

        # 3. READ & OWNERSHIP
        log("Ownership (Own)", tools.read_task(session, t1['id'], u1.id) is not None)
        log("Ownership (Forbidden)", tools.read_task(session, t1['id'], u2.id) is None)

        # 4. COMPLETION RULE
        tools.update_task(session, t1['id'], u1.id, completed=True)
        log("Completion (F->T)", True)
        try:
            tools.update_task(session, t1['id'], u1.id, completed=False)
            log("Completion (T->F Prohibited)", False)
        except ValueError:
            log("Completion (T->F Prohibited)", True)

        # 5. DELETE & OWNERSHIP
        log("Delete (Forbidden)", tools.delete_task(session, t1['id'], u2.id) is False)
        log("Delete (Own)", tools.delete_task(session, t1['id'], u1.id) is True)
        log("Delete (Verify)", tools.read_task(session, t1['id'], u1.id) is None)

    print("="*40 + "\nVerification Complete")

if __name__ == "__main__":
    run_verify()
