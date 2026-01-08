"""
MCP Server for Phase 3 Todo AI Chatbot
Implements the locked CRUD operations spec via MCP protocol
"""
import json
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException
from sqlmodel import Session
from .database import get_session
from .mcp_tools import TaskMCPTools


class MCPServer:
    """
    MCP Server implementation for Task CRUD operations
    """

    def __init__(self):
        self.tools = TaskMCPTools()

    def handle_create_task(self, session: Session, user_id: str, title: str) -> Dict[str, Any]:
        """
        MCP Tool: Create a new task
        """
        try:
            result = self.tools.create_task(session, user_id, title)
            return {"success": True, "task": result}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_read_task(self, session: Session, task_id: int, user_id: str) -> Dict[str, Any]:
        """
        MCP Tool: Read a task
        """
        try:
            result = self.tools.read_task(session, task_id, user_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Task not found or access denied")
            return {"success": True, "task": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_update_task(
        self,
        session: Session,
        task_id: int,
        user_id: str,
        new_title: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        MCP Tool: Update a task
        """
        try:
            result = self.tools.update_task(session, task_id, user_id, new_title, completed)
            if result is None:
                raise HTTPException(status_code=404, detail="Task not found or access denied")
            return {"success": True, "task": result}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def handle_delete_task(self, session: Session, task_id: int, user_id: str) -> Dict[str, Any]:
        """
        MCP Tool: Delete a task
        """
        try:
            success = self.tools.delete_task(session, task_id, user_id)
            if not success:
                raise HTTPException(status_code=404, detail="Task not found or access denied")
            return {"success": True, "message": "Task deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Initialize the MCP server instance
mcp_server = MCPServer()