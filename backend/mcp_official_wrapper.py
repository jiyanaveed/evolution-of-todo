"""
MCP Official Wrapper for Phase 3 Todo AI Chatbot
Provides the same interface as the old mcp_server but uses the new official MCP implementation
"""
import json
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException
from sqlmodel import Session
from .database import get_session
from .mcp_tools import TaskMCPTools


class MCPOfficialWrapper:
    """
    MCP Official Wrapper implementation for Task CRUD operations
    Provides the same interface as the old MCPServer but uses the new tools
    """

    def __init__(self):
        self.tools = TaskMCPTools()

    def handle_add_task(self, session: Session, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP Tool: add_task
        Purpose: Create a new task
        Parameters: user_id (string, required), title (string, required), description (string, optional)
        Returns: task_id, status, title
        """
        try:
            result = self.tools.create_task(session, user_id, title, description)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_list_tasks(self, session: Session, user_id: str, status: Optional[str] = None) -> Any:
        """
        MCP Tool: list_tasks
        Purpose: Retrieve tasks from the list
        Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
        Returns: Array of task objects
        """
        try:
            result = self.tools.list_tasks(session, user_id, status)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_complete_task(self, session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: complete_task
        Purpose: Mark a task as complete
        Parameters: user_id (string, required), task_id (integer, required)
        Returns: task_id, status, title
        """
        try:
            result = self.tools.complete_task(session, user_id, task_id)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_delete_task(self, session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: delete_task
        Purpose: Remove a task from the list
        Parameters: user_id (string, required), task_id (integer, required)
        Returns: task_id, status, title
        """
        try:
            result = self.tools.delete_task(session, user_id, task_id)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_update_task(self, session: Session, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP Tool: update_task
        Purpose: Modify task title or description
        Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
        Returns: task_id, status, title
        """
        try:
            result = self.tools.update_task(session, user_id, task_id, title, description)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Initialize the MCP official wrapper instance
mcp_official_wrapper = MCPOfficialWrapper()