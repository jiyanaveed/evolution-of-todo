"""
Official MCP Server Implementation for Phase 3
Uses the official Model Context Protocol SDK
"""
from mcp.server.fastmcp import FastMCP
from typing import Optional
from sqlmodel import Session
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

# Create MCP server
mcp = FastMCP("Evolution-of-Todo")

# Storage for session (would be database in production)
_sessions: dict = {}


@mcp.tool()
def create_task(title: str, user_id: str) -> dict:
    """
    Create a new task for a user.

    Args:
        title: The task title/description
        user_id: The user ID to create the task for

    Returns:
        Dictionary with task details including ID
    """
    # Import here to avoid circular imports
    from . import crud

    # For demo, use first session available
    # In production, pass session through context
    from .database import get_session
    session = next(get_session())

    task = crud.create_task(session, title=title, description=None, user_id=user_id)
    session.close()

    return {
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "user_id": task.user_id
        }
    }


@mcp.tool()
def get_task(task_id: int, user_id: str) -> dict:
    """
    Get a specific task by ID.

    Args:
        task_id: The task ID
        user_id: The user ID (for authorization)

    Returns:
        Task details or error if not found
    """
    from . import crud
    from .database import get_session
    session = next(get_session())

    task = crud.get_task_by_user(session, task_id, user_id)
    session.close()

    if not task:
        return {"success": False, "error": "Task not found"}

    return {
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "user_id": task.user_id
        }
    }


@mcp.tool()
def list_tasks(user_id: str) -> dict:
    """
    List all tasks for a user.

    Args:
        user_id: The user ID

    Returns:
        List of all tasks for the user
    """
    from . import crud
    from .database import get_session
    session = next(get_session())

    tasks = crud.get_tasks_by_user(session, user_id)
    session.close()

    return {
        "success": True,
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "completed": t.completed,
                "user_id": t.user_id
            }
            for t in tasks
        ]
    }


@mcp.tool()
def update_task(task_id: int, user_id: str, new_title: Optional[str] = None, completed: Optional[bool] = None) -> dict:
    """
    Update a task (rename or complete).

    Args:
        task_id: The task ID
        user_id: The user ID
        new_title: New title for the task (optional)
        completed: New completion status (optional)

    Returns:
        Updated task details or error
    """
    from . import crud
    from .database import get_session
    session = next(get_session())

    task = crud.update_task(session, task_id, user_id, new_title, completed)
    session.close()

    if not task:
        return {"success": False, "error": "Task not found"}

    return {
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "user_id": task.user_id
        }
    }


@mcp.tool()
def delete_task(task_id: int, user_id: str) -> dict:
    """
    Delete a task.

    Args:
        task_id: The task ID
        user_id: The user ID

    Returns:
        Success message or error
    """
    from . import crud
    from .database import get_session
    session = next(get_session())

    success = crud.delete_task(session, task_id, user_id)
    session.close()

    if not success:
        return {"success": False, "error": "Task not found"}

    return {
        "success": True,
        "message": f"Task {task_id} deleted successfully"
    }


@mcp.resource("todos://{user_id}")
def user_todos(user_id: str) -> str:
    """
    Get all todos for a user as a resource.

    Args:
        user_id: The user ID

    Returns:
        JSON string of user's todos
    """
    result = list_tasks(user_id)
    import json
    return json.dumps(result.get("tasks", []), indent=2)


@mcp.prompt()
def todo_assistance_prompt() -> str:
    """
    Generate a prompt for analyzing and improving the todo list.
    """
    return """Please review the current todo list and provide:
1. Overall assessment of task completion status
2. Suggestions for prioritization
3. Any patterns or insights about the tasks
4. Recommendations for organizing or consolidating similar tasks"""


def run_mcp_server():
    """Run the MCP server"""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    run_mcp_server()
