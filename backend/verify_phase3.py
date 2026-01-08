"""
PHASE 3 VERIFICATION SCRIPT
Validates the AI Todo Chatbot implementation against the locked specification.
- Tolls: create, get, list, update, delete
- Rules: Two-Step Mutation (Delete/Rename), Completion (No True->False), Ownership
"""
import sys
import os
import uuid
import json

# Setup environment to import backend modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from sqlmodel import Session, create_engine, SQLModel, select
    import models
    from models import Task, User, Message
    import crud
    from crud import create_user
    from .mcp_official_wrapper import mcp_official_wrapper as mcp_server
except ImportError as e:
    print(f"❌ Critical Error: Missing backend modules. Details: {e}")
    sys.exit(1)

# --- HELPER FUNCTIONS ---

def log_test(name, success, message=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {name}" + (f": {message}" if message else ""))

def create_test_db():
    db_path = "phase3_verify.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(engine)
    return engine

# --- TEST SUITE ---

def run_verify_suite():
    print("🚀 Starting Phase 3 Authoritative Verification Suite\n" + "="*50)
    engine = create_test_db()

    with Session(engine) as session:
        # 1. SETUP - Two Isolated Users
        user_a = create_user(session, "user_a@example.com", "pass")
        user_b = create_user(session, "user_b@example.com", "pass")
        print(f"Setup: Created User A ({user_a.id}) and User B ({user_b.id})")

        # 2. CREATE TASK (Tool: create_todo_task)
        print("\n[Tool: create_todo_task]")
        try:
            res = mcp_server.handle_create_task(session, user_a.id, "Task A1")
            task_a1 = res['task']
            log_test("Standard Creation", res['success'], f"Task ID {task_a1['id']} created.")
        except Exception as e:
            log_test("Standard Creation", False, str(e))

        # 3. EDGE CASE: Empty Title
        try:
            mcp_server.handle_create_task(session, user_a.id, "   ")
            log_test("Validation: Empty Title", False, "Should have rejected empty title.")
        except Exception:
            log_test("Validation: Empty Title", True, "Rejected empty title correctly.")

        # 4. READ TASK (Tool: get_todo_task)
        print("\n[Tool: get_todo_task]")
        try:
            res = mcp_server.handle_read_task(session, task_a1['id'], user_a.id)
            log_test("Ownership: Read Own Task", res['success'])
        except Exception as e:
            log_test("Ownership: Read Own Task", False, str(e))

        # 5. SECURITY: Cross-User Access (Ownership Rule)
        try:
            mcp_server.handle_read_task(session, task_a1['id'], user_b.id)
            log_test("Security: Cross-User Read", False, "User B accessed User A's task.")
        except Exception:
            log_test("Security: Cross-User Read", True, "Access Denied confirmed.")

        # 6. UPDATE: Rename (Two-Step Mutation Rule applies at Orchestration, Tool handles mutation)
        print("\n[Tool: update_todo_task]")
        try:
            res = mcp_server.handle_update_task(session, task_a1['id'], user_a.id, new_title="Updated A1")
            log_test("Standard Update: Rename", res['success'])
        except Exception as e:
            log_test("Standard Update: Rename", False, str(e))

        # 7. COMPLETION RULE: False -> True
        try:
            res = mcp_server.handle_update_task(session, task_a1['id'], user_a.id, completed=True)
            log_test("Completion Rule: False -> True", res['success'])
        except Exception as e:
            log_test("Completion Rule: False -> True", False, str(e))

        # 8. COMPLETION RULE: True -> False (LOCKED Rule)
        try:
            mcp_server.handle_update_task(session, task_a1['id'], user_a.id, completed=False)
            # Fetch to check if it's still True
            check_res = mcp_server.handle_read_task(session, task_a1['id'], user_a.id)
            is_still_true = check_res['task']['completed'] == True
            log_test("Completion Rule: True -> False (Prohibited)", is_still_true, "Task remained completed.")
        except Exception:
             log_test("Completion Rule: True -> False (Prohibited)", True, "Rejected via constraint.")

        # 9. LIST TASKS (Tool: list_todo_tasks)
        print("\n[Tool: list_todo_tasks]")
        # Since handle_list_todo_tasks isn't in current main API, we check if users get isolated lists
        # We manually use the MCP tools logic or crud
        import crud
        tasks_a = crud.get_tasks_by_user(session, user_a.id)
        tasks_b = crud.get_tasks_by_user(session, user_b.id)
        log_test("Isolation: List User A", len(tasks_a) > 0)
        log_test("Isolation: List User B", len(tasks_b) == 0)

        # 10. DELETE TASK (Tool: delete_todo_task)
        print("\n[Tool: delete_todo_task]")
        # 11. SECURITY: Cross-User Delete
        try:
            mcp_server.handle_delete_task(session, task_a1['id'], user_b.id)
            log_test("Security: Cross-User Delete", False, "User B deleted User A's task.")
        except Exception:
            log_test("Security: Cross-User Delete", True, "Access Denied confirmed.")

        # 12. Standard Deletion
        try:
            res = mcp_server.handle_delete_task(session, task_a1['id'], user_a.id)
            log_test("Standard Deletion", res['success'])
        except Exception as e:
            log_test("Standard Deletion", False, str(e))

    print("\n" + "="*50 + "\n🚀 Verification Suite Complete")

if __name__ == "__main__":
    run_verify_suite()
    # Cleanup
    if os.path.exists("phase3_verify.db"):
        os.remove("phase3_verify.db")
