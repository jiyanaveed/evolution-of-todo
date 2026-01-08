"""
MCP Tools for Phase 3 Todo AI Chatbot
Implements the locked CRUD operations spec
"""
from typing import Optional, Dict, Any, List
from .models import Task, TaskResponse
from .crud import create_task as crud_create_task
from .crud import get_task_by_user as crud_get_task_by_user
from .crud import update_task as crud_update_task
from .crud import delete_task as crud_delete_task
from .crud import get_tasks_by_user as crud_get_tasks_by_user
from sqlmodel import Session


class TaskMCPTools:
    """
    MCP Tools implementation for Task CRUD operations following the locked spec
    """

    @staticmethod
    def create_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP Tool: add_task
        Purpose: Create a new task
        Parameters: user_id (string, required), title (string, required), description (string, optional)
        Returns: task_id, status, title
        Example Input: {"user_id": "ziakhan", "title": "Buy groceries", "description": "Milk, eggs, bread"}
        Example Output: {"task_id": 5, "status": "created", "title": "Buy groceries"}
        """
        # Validate input
        if not title or not title.strip():
            raise ValueError("Title must be non-empty and contain at least one non-whitespace character")

        # Create task using existing CRUD function
        task = crud_create_task(session, title.strip(), description, user_id)

        # Return in the specified format
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }

    @staticmethod
    def list_tasks(session: Session, user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        MCP Tool: list_tasks
        Purpose: Retrieve tasks from the list
        Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
        Returns: Array of task objects
        Example Input: {"user_id": "ziakhan", "status": "pending"}
        Example Output: [{"id": 1, "title": "Buy groceries", "completed": false}, ...]
        """
        # Get all tasks for the user
        tasks = crud_get_tasks_by_user(session, user_id)

        # Filter based on status if provided
        if status == "pending":
            tasks = [task for task in tasks if not task.completed]
        elif status == "completed":
            tasks = [task for task in tasks if task.completed]
        # If status is "all" or None, return all tasks

        # Format the tasks as specified
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            })

        return result

    @staticmethod
    def complete_task(session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: complete_task
        Purpose: Mark a task as complete
        Parameters: user_id (string, required), task_id (integer, required)
        Returns: task_id, status, title
        Example Input: {"user_id": "ziakhan", "task_id": 3}
        Example Output: {"task_id": 3, "status": "completed", "title": "Call mom"}
        """
        # Update the task to mark as completed
        updated_task = crud_update_task(session, task_id, user_id, completed=True)

        if updated_task is None:
            raise ValueError(f"Task with id {task_id} not found or access denied")

        # Return in the specified format
        return {
            "task_id": updated_task.id,
            "status": "completed",
            "title": updated_task.title
        }

    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: delete_task
        Purpose: Remove a task from the list
        Parameters: user_id (string, required), task_id (integer, required)
        Returns: task_id, status, title
        Example Input: {"user_id": "ziakhan", "task_id": 2}
        Example Output: {"task_id": 2, "status": "deleted", "title": "Old task"}
        """
        # Get the task first to return its title in the response
        task = crud_get_task_by_user(session, task_id, user_id)

        if task is None:
            raise ValueError(f"Task with id {task_id} not found or access denied")

        # Delete the task
        success = crud_delete_task(session, task_id, user_id)

        if not success:
            raise ValueError(f"Failed to delete task with id {task_id}")

        # Return in the specified format
        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }

    @staticmethod
    def update_task(session: Session, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP Tool: update_task
        Purpose: Modify task title or description
        Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
        Returns: task_id, status, title
        Example Input: {"user_id": "ziakhan", "task_id": 1, "title": "Buy groceries and fruits"}
        Example Output: {"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
        """
        # Update the task
        updated_task = crud_update_task(session, task_id, user_id, title=title, description=description)

        if updated_task is None:
            raise ValueError(f"Task with id {task_id} not found or access denied")

        # Return in the specified format
        return {
            "task_id": updated_task.id,
            "status": "updated",
            "title": updated_task.title
        }