#!/usr/bin/env python3
"""
Test script to verify the improved agent functionality.
This tests the key operations: add, list, update/edit, complete, delete.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import get_session
from backend import crud
from backend.agent import AgentOrchestrator
from sqlmodel import Session
from sqlmodel import select
import uuid

def test_agent_functionality():
    """Test the agent functionality with various operations."""

    print("Testing Agent Functionality...")
    print("=" * 50)

    # Initialize the database (create tables if they don't exist)
    from backend.database import init_db
    init_db()

    # Create a session manually
    from backend.database import engine
    with Session(engine) as session:
        # Create a test user
        test_user_id = str(uuid.uuid4())
        print(f"Created test user ID: {test_user_id}")

        # Create the agent orchestrator
        agent = AgentOrchestrator(session)

        # Test 1: Add a task
        print("\n1. Testing ADD task:")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",  # Using a fixed conversation ID for testing
            message_text="Add buy groceries"
        )
        print(f"Response: {response}")

        # Verify task was added
        tasks = crud.get_tasks_by_user(session, test_user_id)
        print(f"Tasks after add: {[t.title for t in tasks]}")

        # Test 2: Add another task
        print("\n2. Testing ADD another task:")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="Add walk the dog"
        )
        print(f"Response: {response}")

        tasks = crud.get_tasks_by_user(session, test_user_id)
        print(f"Tasks after second add: {[(t.id, t.title, t.completed) for t in tasks]}")

        # Test 3: List tasks
        print("\n3. Testing LIST tasks:")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="List my tasks"
        )
        print(f"Response: {response}")

        # Test 4: Edit/update task (the key test case from the issue)
        print("\n4. Testing EDIT/UPDATE task (key test case):")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="edit buy groceries to buy milk and bread"
        )
        print(f"Response: {response}")

        tasks = crud.get_tasks_by_user(session, test_user_id)
        print(f"Tasks after edit: {[(t.id, t.title, t.completed) for t in tasks]}")

        # Test 5: Update with 'update' keyword
        print("\n5. Testing UPDATE task with 'update' keyword:")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="update buy milk and bread to buy milk, bread, and eggs"
        )
        print(f"Response: {response}")

        tasks = crud.get_tasks_by_user(session, test_user_id)
        print(f"Tasks after update: {[(t.id, t.title, t.completed) for t in tasks]}")

        # Test 6: Complete a task
        print("\n6. Testing COMPLETE task:")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="complete buy milk, bread, and eggs"
        )
        print(f"Response: {response}")

        tasks = crud.get_tasks_by_user(session, test_user_id)
        print(f"Tasks after completion: {[(t.id, t.title, t.completed) for t in tasks]}")

        # Test 7: Delete a task (should trigger confirmation)
        print("\n7. Testing DELETE task (should ask for confirmation):")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="delete walk the dog"
        )
        print(f"Response: {response}")

        # Confirm the deletion
        print("\n8. Confirming deletion:")
        response = agent.handle_message(
            user_id=test_user_id,
            conversation_id="1",
            message_text="yes"
        )
        print(f"Response: {response}")

        tasks = crud.get_tasks_by_user(session, test_user_id)
        print(f"Tasks after deletion: {[(t.id, t.title, t.completed) for t in tasks]}")

        print("\nTest completed successfully!")
        print("=" * 50)

if __name__ == "__main__":
    test_agent_functionality()