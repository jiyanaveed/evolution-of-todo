from fastapi import FastAPI, Depends, HTTPException, Body
from sqlmodel import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi import Body
from dotenv import load_dotenv
import os
import logging
import sys

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

from .database import get_session, init_db
from backend.models import (
    TaskResponse, TaskCreate, TaskUpdate,
    UserCreate, UserLogin, UserResponse,
    Token, TokenData,
    MessageResponse
)
from backend import crud
from backend.auth import (
    get_current_user, authenticate_user,
    create_access_token
)
from backend.better_auth import (
    better_auth,
    get_current_user as get_current_better_auth_user,
    register_better_auth_user,
    login_better_auth_user
)
from backend.mcp_official_wrapper import mcp_official_wrapper as mcp_server
from backend.agents_sdk import create_todo_agent, run_todo_agent, run_todo_agent_with_mcp_tools
from backend.agent import AgentOrchestrator
from backend.models import (
    TaskResponse, TaskCreate, TaskUpdate,
    UserCreate, UserLogin, UserResponse,
    Token, TokenData,
    MessageResponse,
    ChatRequest, ChatResponse
)
from backend.database import get_session, init_db
from dotenv import load_dotenv
import os
import uuid

# Load the .env file in the backend folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(
    title="Evolution of Todo - Phase 2 Backend",
    version="1.0.0",
    description="A FastAPI backend for the Evolution of Todo application"
)


# Add CORS middleware to allow requests from localhost:3000 and localhost:3001
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    Initialize the database on application startup.
    """
    init_db()


# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = crud.get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Create new user
    user = crud.create_user(session, user_create.email, user_create.password)
    return UserResponse(id=user.id, email=user.email, created_at=user.created_at)


@app.post("/auth/login", response_model=Token)
def login_user(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Login a user and return access token.
    """
    user = authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.id, "email": user.email})
    return Token(access_token=access_token, token_type="bearer")


@app.get("/auth/me", response_model=UserResponse)
def read_users_me(current_user: TokenData = Depends(get_current_user)):
    """
    Get current user's information.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at
    )


# Better Auth endpoints (unified authentication)
@app.post("/api/auth/register")
def register_user_better_auth(
    email: str = Body(...),
    password: str = Body(...),
    session: Session = Depends(get_session)
):
    """
    Register a new user using Better Auth protocol.
    Compatible with Better Auth frontend authentication.
    """
    result = register_better_auth_user(email, password, session)
    return result


@app.post("/api/auth/login")
def login_user_better_auth(
    email: str = Body(...),
    password: str = Body(...),
    session: Session = Depends(get_session)
):
    """
    Login a user using Better Auth protocol.
    Compatible with Better Auth frontend authentication.
    """
    result = login_better_auth_user(email, password, session)
    return result


@app.get("/api/auth/me")
def read_users_me_better_auth(
    current_user = Depends(get_current_better_auth_user)
):
    """
    Get current user's information using Better Auth.
    """
    return {
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "createdAt": current_user.created_at.isoformat() if current_user.created_at else None
        }
    }


# Task endpoints with user_id in path (required pattern: /api/{user_id}/tasks/{id})
@app.get("/api/{user_id}/tasks", response_model=List[TaskResponse])
def read_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_better_auth_user)
):
    """
    Retrieve all tasks for a user from the database.
    """
    # Verify the requesting user matches the user_id in the path
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    tasks = crud.get_tasks_by_user(session, current_user.id)
    return tasks


@app.post("/api/{user_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    user_id: str,
    task_create: TaskCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_better_auth_user)
):
    """
    Create a new task for a user in the database.
    """
    # Verify the requesting user matches the user_id in the path
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    task = crud.create_task(session, title=task_create.title, description=None, user_id=current_user.id)
    return task


@app.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def read_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_better_auth_user)
):
    """
    Retrieve a specific task by ID for a user from the database.
    """
    # Verify the requesting user matches the user_id in the path
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    task = crud.get_task_by_user(session, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate = Body(...),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_better_auth_user)
):
    """
    Update an existing task's title for a user in the database.
    """
    # Verify the requesting user matches the user_id in the path
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    task = crud.update_task(
        session,
        task_id,
        current_user.id,
        title=task_update.title,
        completed=task_update.completed
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/api/{user_id}/tasks/{task_id}", status_code=204)
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_better_auth_user)
):
    """
    Delete a task from the database by ID for a user.
    """
    # Verify the requesting user matches the user_id in the path
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    success = crud.delete_task(session, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return  # Return empty response for 204 status


@app.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_better_auth_user)
):
    """
    Toggle the completion status of a task in the database for a user.
    """
    # Verify the requesting user matches the user_id in the path
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    task = crud.toggle_task_completion(session, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Evolution of Todo - Phase 2 Backend with Authentication is running!"}


# Chat API Endpoint according to specification
@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user = Depends(get_current_better_auth_user),
    session: Session = Depends(get_session)
):
    """
    Chat API Endpoint
    Method: POST
    Endpoint: /api/{user_id}/chat
    Description: Send message & get AI response

    Request:
    - conversation_id (integer, optional): Existing conversation ID (creates new if not provided)
    - message (string, required): User's natural language message

    Response:
    - conversation_id (integer): The conversation ID
    - response (string): AI assistant's response
    - tool_calls (array): List of MCP tools invoked
    """
    logger.info(f"Chat endpoint called - user_id: {user_id}, message: {chat_request.message[:50]}...")
    try:
        # Verify the requesting user matches the user_id in the path
        if str(current_user.id) != user_id:
            logger.warning(f"Access denied - current_user: {current_user.id}, requested_user: {user_id}")
            raise HTTPException(status_code=403, detail="Access denied")

        logger.debug(f"User verified, processing conversation")
        # Get or create conversation
        conversation_id = chat_request.conversation_id
        logger.debug(f"Conversation ID from request: {conversation_id}")
        if conversation_id is None:
            # Create new conversation
            logger.info(f"Creating new conversation for user {user_id}")
            conversation = crud.create_conversation(session, user_id)
            conversation_id = conversation.id
            logger.info(f"Created conversation with ID: {conversation_id}")
        else:
            # Verify conversation belongs to user
            existing_conversation = crud.get_conversation(session, conversation_id, user_id)
            if not existing_conversation:
                raise HTTPException(status_code=404, detail="Conversation not found or access denied")

        # Fetch conversation history from database (for agent context)
        conversation_history = crud.get_messages(session, conversation_id, user_id)

        # Build message array for agent (history + new message)
        messages = []
        for msg in conversation_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Use Agent Orchestrator to process the message with MCP tools
        try:
            # Create the agent orchestrator instance
            agent_orchestrator = AgentOrchestrator(session)

            # Process the message through the orchestrator
            # Make sure conversation_id is not None before passing to agent
            if conversation_id is None:
                # This shouldn't happen since we create conversation_id above if it's None
                response = "Error: Conversation ID is required for agent operations."
            else:
                response = agent_orchestrator.handle_message(
                    user_id=user_id,
                    conversation_id=str(conversation_id),  # Pass as string since agent will convert internally
                    message_text=chat_request.message
                )
            tool_calls = []  # Tool calls are handled internally by the orchestrator

            logger.info(f"Agent response received: {response[:100]}...")
        except Exception as e:
            # Fallback to rule-based processing if agents fail
            logger.error(f"Agent processing failed: {e}", exc_info=True)
            response = f"I received your message: '{chat_request.message}'. However, I'm unable to process it right now due to an error. Please try again or contact support if the issue persists."
            tool_calls = []

        # Return response according to specification
        # Note: Messages are already persisted by the AgentOrchestrator
        return ChatResponse(
            conversation_id=conversation_id,
            response=response,
            tool_calls=tool_calls
        )
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Catch any other errors in the entire process
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error occurred while processing your request")


# MCP (Model Context Protocol) endpoints for Phase 3 AI Chatbot (Updated to match specification)
@app.post("/mcp/add_task")
def mcp_add_task(
    user_id: str = Body(..., embed=True),
    title: str = Body(..., embed=True),
    description: Optional[str] = Body(None, embed=True),
    current_user = Depends(get_current_better_auth_user),
    session: Session = Depends(get_session)
):
    """
    MCP Tool: add_task
    Purpose: Create a new task
    Parameters: user_id (string, required), title (string, required), description (string, optional)
    Returns: task_id, status, title
    """
    # Verify the requesting user matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return mcp_server.handle_add_task(session, user_id, title, description)


@app.post("/mcp/list_tasks")
def mcp_list_tasks(
    user_id: str = Body(..., embed=True),
    status: Optional[str] = Body(None, embed=True),
    current_user = Depends(get_current_better_auth_user),
    session: Session = Depends(get_session)
):
    """
    MCP Tool: list_tasks
    Purpose: Retrieve tasks from the list
    Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
    Returns: Array of task objects
    """
    # Verify the requesting user matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return mcp_server.handle_list_tasks(session, user_id, status)


@app.post("/mcp/complete_task")
def mcp_complete_task(
    user_id: str = Body(..., embed=True),
    task_id: int = Body(..., embed=True),
    current_user = Depends(get_current_better_auth_user),
    session: Session = Depends(get_session)
):
    """
    MCP Tool: complete_task
    Purpose: Mark a task as complete
    Parameters: user_id (string, required), task_id (integer, required)
    Returns: task_id, status, title
    """
    # Verify the requesting user matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return mcp_server.handle_complete_task(session, user_id, task_id)


@app.post("/mcp/delete_task")
def mcp_delete_task(
    user_id: str = Body(..., embed=True),
    task_id: int = Body(..., embed=True),
    current_user = Depends(get_current_better_auth_user),
    session: Session = Depends(get_session)
):
    """
    MCP Tool: delete_task
    Purpose: Remove a task from the list
    Parameters: user_id (string, required), task_id (integer, required)
    Returns: task_id, status, title
    """
    # Verify the requesting user matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return mcp_server.handle_delete_task(session, user_id, task_id)


@app.post("/mcp/update_task")
def mcp_update_task(
    user_id: str = Body(..., embed=True),
    task_id: int = Body(..., embed=True),
    title: Optional[str] = Body(None, embed=True),
    description: Optional[str] = Body(None, embed=True),
    current_user = Depends(get_current_better_auth_user),
    session: Session = Depends(get_session)
):
    """
    MCP Tool: update_task
    Purpose: Modify task title or description
    Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
    Returns: task_id, status, title
    """
    # Verify the requesting user matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return mcp_server.handle_update_task(session, user_id, task_id, title, description)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


