#!/usr/bin/env python3
"""
Test script to debug the authentication and update functionality
"""
import sys
import os
import uuid
from sqlmodel import Session, select
from datetime import datetime
import bcrypt

# Add the parent directory to the path so we can import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import Task, User
from backend.database import engine, init_db
from backend.crud import create_task, update_task, get_task_by_user, get_user_by_id, create_user

def test_auth_and_update_functionality():
    print("Testing authentication and update functionality...")

    # Initialize the database
    init_db()

    # Create a session
    with Session(engine) as session:
        # Create a test user
        user_id = str(uuid.uuid4())
        test_email = f"test_{uuid.uuid4()}@example.com"
        hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        test_user = User(
            id=user_id,
            email=test_email,
            password_hash=hashed_password,
            created_at=datetime.utcnow(),
            is_active=True
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        print(f"Created test user with ID: {user_id}")

        # Create a test task for this user
        task = create_task(session, "Original Task Title", user_id)
        print(f"Created task: ID={task.id}, Title='{task.title}', Completed={task.completed}")

        # Try to update the task with the correct user_id
        print(f"Attempting to update task {task.id} for user {user_id}")
        updated_task = update_task(session, task.id, user_id, title="Updated Task Title", completed=True)

        if updated_task:
            print(f"SUCCESS: Updated task: ID={updated_task.id}, Title='{updated_task.title}', Completed={updated_task.completed}")
        else:
            print("FAILED: Update returned None - task might not exist or user doesn't have permission")

            # Let's debug by checking if the task exists for the user
            task_check = get_task_by_user(session, task.id, user_id)
            if task_check:
                print(f"DEBUG: Task found for user - ID={task_check.id}, Title='{task_check.title}'")
            else:
                print("DEBUG: Task not found for user - possible permission issue")

                # Check if task exists at all
                all_tasks = session.exec(select(Task)).all()
                print(f"DEBUG: All tasks in DB: {[(t.id, t.user_id, t.title) for t in all_tasks]}")

                # Check if user exists
                user_check = get_user_by_id(session, user_id)
                if user_check:
                    print(f"DEBUG: User exists - ID={user_check.id}, Email={user_check.email}")
                else:
                    print("DEBUG: User does not exist in DB")

        # Now test with wrong user_id to confirm the security works
        print("\nTesting with wrong user_id (should fail)...")
        wrong_user_id = str(uuid.uuid4())
        failed_update = update_task(session, task.id, wrong_user_id, title="Should Not Work", completed=False)
        if failed_update is None:
            print("SUCCESS: Update with wrong user_id correctly failed (security working)")
        else:
            print("ISSUE: Update with wrong user_id succeeded (security issue)")

if __name__ == "__main__":
    test_auth_and_update_functionality()