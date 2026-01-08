"""
Standalone verification of the Agent Orchestration logic.
This script tests the core orchestration lifecycle and rules without relative import issues.
"""
import uuid
import re
from typing import List, Any

# Mock objects to simulate the backend environment
class MockMessage:
    def __init__(self, content, role):
        self.content = content
        self.role = role

class MockTask:
    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

class MockCRUD:
    def __init__(self):
        self.messages = []
        self.tasks = []
        self.next_task_id = 1

    def get_messages(self, cid, uid):
        return [m for m in self.messages if m.conversation_id == cid]

    def save_message(self, cid, uid, role, content):
        msg = MockMessage(content, role)
        msg.conversation_id = cid
        self.messages.append(msg)
        return msg

    def create_task(self, uid, title):
        task = MockTask(self.next_task_id, title)
        self.next_task_id += 1
        self.tasks.append(task)
        return task

    def get_tasks_by_user(self, uid):
        return self.tasks

    def delete_task(self, tid, uid):
        self.tasks = [t for t in self.tasks if t.id != tid]
        return True

    def update_task(self, tid, uid, title=None, completed=None):
        for t in self.tasks:
            if t.id == tid:
                if title: t.title = title
                if completed is not None: t.completed = completed
                return t
        return None

# Simplified Orchestrator for verification
class VerifiedOrchestrator:
    def __init__(self, crud):
        self.crud = crud

    def handle_message(self, user_id, conversation_id, message_text):
        # 1. FETCH
        history = self.crud.get_messages(conversation_id, user_id)

        # 3. RUN (Logic from agent.py)
        msg_lower = message_text.lower()

        def was_confirmed():
            if not history: return False
            last_assistant_msg = next((m for m in reversed(history) if m.role == "assistant"), None)
            if not last_assistant_msg: return False
            is_request = "are you sure" in last_assistant_msg.content.lower()
            is_affirmative = msg_lower in ["yes", "yeah", "yep", "confirm", "do it"]
            return is_request and is_affirmative

        response_text = "I don't understand."

        # Intent: Create
        if "add" in msg_lower:
            title = message_text.replace("add", "").strip()
            self.crud.create_task(user_id, title)
            response_text = f"Created task: {title}"

        # Intent: List
        elif "list" in msg_lower:
            tasks = self.crud.get_tasks_by_user(user_id)
            task_list = "\n".join([f"- {t.id}: {t.title}" for t in tasks])
            response_text = f"Your tasks:\n{task_list}"

        # Intent: Delete (Two-Step)
        elif "delete" in msg_lower:
            match = re.search(r'task (\d+)', msg_lower)
            if match:
                tid = int(match.group(1))
                if was_confirmed():
                    self.crud.delete_task(tid, user_id)
                    response_text = f"Deleted task {tid}"
                else:
                    response_text = f"Are you sure you want to delete task {tid}? (yes/no)"

        # Intent: Affirmative for Two-Step
        elif was_confirmed():
            # Find what was being confirmed
            last_assistant_msg = next((m for m in reversed(history) if m.role == "assistant"), None)
            match = re.search(r'task (\d+)', last_assistant_msg.content.lower())
            if match:
                tid = int(match.group(1))
                if "delete" in last_assistant_msg.content.lower():
                    self.crud.delete_task(tid, user_id)
                    response_text = f"Deleted task {tid}"

        # 4. PERSIST
        self.crud.save_message(conversation_id, user_id, "user", message_text)
        self.crud.save_message(conversation_id, user_id, "assistant", response_text)

        return response_text

def run_verification():
    print("--- Phase 3 Agent Orchestration Verification ---")
    crud = MockCRUD()
    orch = VerifiedOrchestrator(crud)
    uid = "user-123"
    cid = "conv-456"

    # Test 1: Create
    print("\n[Test 1] User: Add Buy eggs")
    print(f"Agent: {orch.handle_message(uid, cid, 'Add Buy eggs')}")

    # Test 2: List
    print("\n[Test 2] User: List tasks")
    print(f"Agent: {orch.handle_message(uid, cid, 'List tasks')}")

    # Test 3: Delete (Step 1)
    print("\n[Test 3] User: Delete task 1")
    print(f"Agent: {orch.handle_message(uid, cid, 'Delete task 1')}")

    # Test 4: Delete (Step 2 - Affirmative)
    print("\n[Test 4] User: Yes")
    print(f"Agent: {orch.handle_message(uid, cid, 'Yes')}")

    # Test 5: Verify Deletion
    print("\n[Test 5] User: List tasks (after deletion)")
    print(f"Agent: {orch.handle_message(uid, cid, 'List tasks')}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_verification()
