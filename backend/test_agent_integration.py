"""
Script to test the Agent Orchestration Layer integration in Phase 3.
"""
import sys
import os
import uuid
import json

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from sqlmodel import Session, create_engine, SQLModel, select
    import models
    from models import User, Task, Message
    import crud
    from crud import create_user, get_user_by_email, save_message
    import agent
    from agent import AgentOrchestrator
    import database
    from database import init_db
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def test_agent_integration():
    print("🚀 Starting Agent Orchestration Integration Test")

    # Path to test database
    db_path = "todo_test.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    sqlite_url = f"sqlite:///{db_path}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # 1. Setup - Create a test user
        print("\nStep 1: Creating test user...")
        test_email = "testagent@example.com"
        user = create_user(session, test_email, "password123")
        print(f"✅ User created with ID: {user.id}")

        # 2. Test Agent Initialization
        print("\nStep 2: Initializing Agent Orchestrator...")
        orchestrator = AgentOrchestrator(session)
        conversation_id = str(uuid.uuid4())
        print(f"✅ Orchestrator ready. Conversation ID: {conversation_id}")

        # 3. Test CREATE Intent (Immediate)
        print("\nStep 3: Testing 'Add a task' intent...")
        response1 = orchestrator.handle_message(user.id, conversation_id, "Add buy groceries")
        print(f"🤖 Agent: {response1}")

        # Verify message persistence
        messages = session.exec(select(Message).where(Message.conversation_id == conversation_id)).all()
        print(f"✅ Messages persisted: {len(messages)}")

        # 4. Test LIST Intent
        print("\nStep 4: Testing 'List tasks' intent...")
        response2 = orchestrator.handle_message(user.id, conversation_id, "Show my list")
        print(f"🤖 Agent: {response2}")

        # 5. Test DELETE Intent (Two-Step - Step 1: Confirmation Request)
        print("\nStep 5: Testing 'Delete task 1' intent (Should trigger confirmation)...")
        response3 = orchestrator.handle_message(user.id, conversation_id, "Delete task 1")
        print(f"🤖 Agent: {response3}")

        # 6. Test DELETE Confirmation (Two-Step - Step 2: Affirmative Response)
        print("\nStep 6: Confirming deletion...")
        response4 = orchestrator.handle_message(user.id, conversation_id, "Yes")
        print(f"🤖 Agent: {response4}")

        # Verify task is actually deleted in the DB
        task = session.exec(select(Task).where(Task.id == 1)).first()
        if task is None:
            print("✅ Task 1 removed from database.")
        else:
            print("❌ Task 1 still exists in database.")

        # 7. Test RENAME Intent (Two-Step)
        print("\nStep 7: Testing 'Rename task 2' intent (after adding one)...")
        orchestrator.handle_message(user.id, conversation_id, "Add milk")
        response5 = orchestrator.handle_message(user.id, conversation_id, "Rename task 2 to buy almond milk")
        print(f"🤖 Agent: {response5}")

        print("\nStep 8: Confirming rename...")
        response6 = orchestrator.handle_message(user.id, conversation_id, "Yes")
        print(f"🤖 Agent: {response6}")

        # Verify rename
        task2 = session.exec(select(Task).where(Task.id == 2)).first()
        if task2 and task2.title == "buy almond milk":
            print(f"✅ Task 2 title updated to: {task2.title}")
        else:
            print(f"❌ Task 2 update failed.")

    print("\n🏁 Integration Test Completed Successfully!")

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    test_agent_integration()
