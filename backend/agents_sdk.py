"""
OpenAI Agents SDK Implementation for Phase 3
Replaces custom agent with official OpenAI Assistants API
"""
from openai import OpenAI
from typing import List, Dict, Any, Optional
from sqlmodel import Session
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()


def get_openai_client():
    """Get OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def create_todo_agent(session: Session, user_id: str):
    """Create and configure the Todo Agent using OpenAI Assistants API"""

    client = get_openai_client()

    # Create an assistant for todo management
    assistant = client.beta.assistants.create(
        name="Todo Assistant",
        description="A helpful assistant that manages todo lists",
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The task title"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task (complete or rename)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The task ID"},
                            "new_title": {"type": "string", "description": "New title for the task (optional)"},
                            "completed": {"type": "boolean", "description": "Completion status (optional)"}
                        },
                        "required": ["task_id"],
                        "anyOf": [
                            {"required": ["new_title"]},
                            {"required": ["completed"]}
                        ]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The task ID to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]
    )

    return assistant


def run_todo_agent(session: Session, user_id: str, message: str) -> str:
    """Run the todo agent with a user message using OpenAI Assistants API"""

    client = get_openai_client()

    # Create a thread for this conversation
    thread = client.beta.threads.create()

    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=create_todo_agent(session, user_id).id,
        instructions=f"You are a helpful todo list assistant. The current user ID is {user_id}. "
                    "Use the available tools to manage tasks. "
                    "For destructive operations (delete, rename), always ask for confirmation first, "
                    "and only proceed after the user explicitly confirms with 'yes', 'confirm', or similar."
    )

    # Wait for the run to complete
    while run.status in ["queued", "in_progress"]:
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Handle tool calls if any
    if run.status == "requires_action" and run.required_action.type == "submit_tool_outputs":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls

        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Execute the function based on the function name
            if function_name == "create_task":
                from . import crud
                task = crud.create_task(session, title=function_args["title"], description=None, user_id=user_id)
                output = {"id": task.id, "title": task.title, "completed": task.completed}
            elif function_name == "list_tasks":
                from . import crud
                tasks = crud.get_tasks_by_user(session, user_id)
                output = [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
            elif function_name == "update_task":
                from . import crud
                task = crud.update_task(
                    session,
                    function_args["task_id"],
                    user_id,
                    title=function_args.get("new_title"),
                    completed=function_args.get("completed")
                )
                if task:
                    output = {"id": task.id, "title": task.title, "completed": task.completed}
                else:
                    output = {"error": "Task not found"}
            elif function_name == "delete_task":
                from . import crud
                success = crud.delete_task(session, function_args["task_id"], user_id)
                output = {"success": success}
            else:
                output = {"error": f"Unknown function: {function_name}"}

            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(output)
            })

        # Submit the tool outputs
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )

        # Wait for the run to complete after tool outputs
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Get the messages from the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Extract the assistant's response (last message)
    for msg in messages.data:
        if msg.role == "assistant":
            # Get the content of the message
            if msg.content and len(msg.content) > 0 and msg.content[0].type == "text":
                return msg.content[0].text.value

    return "I couldn't process your request. Please try again."


def run_todo_agent_with_mcp_tools(session: Session, user_id: str, message: str, conversation_history: List[Dict[str, str]]) -> tuple[str, List[Dict[str, Any]]]:
    """
    Run the todo agent with MCP tools using OpenAI Assistants API
    Returns: (response_text, tool_calls_made)
    """
    try:
        client = get_openai_client()

        # Create an assistant with MCP tools
        assistant = client.beta.assistants.create(
            name="Todo Assistant with MCP Tools",
            description="A helpful assistant that manages todo lists using MCP tools",
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Add a new task to the list",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The user ID"},
                                "title": {"type": "string", "description": "The task title"},
                                "description": {"type": "string", "description": "Optional task description"}
                            },
                            "required": ["user_id", "title"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_tasks",
                        "description": "List tasks for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The user ID"},
                                "status": {"type": "string", "description": "Filter by status: 'all', 'pending', or 'completed'"}
                            },
                            "required": ["user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "complete_task",
                        "description": "Mark a task as complete",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The user ID"},
                                "task_id": {"type": "integer", "description": "The task ID to complete"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_task",
                        "description": "Delete a task from the list",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The user ID"},
                                "task_id": {"type": "integer", "description": "The task ID to delete"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update a task title or description",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The user ID"},
                                "task_id": {"type": "integer", "description": "The task ID to update"},
                                "title": {"type": "string", "description": "New title for the task (optional)"},
                                "description": {"type": "string", "description": "New description for the task (optional)"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    }
                }
            ]
        )

        # Create a thread for this conversation
        thread = client.beta.threads.create()

        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=f"You are a helpful todo list assistant. The current user ID is {user_id}. "
                        "Use the available MCP tools to manage tasks. "
                        "For destructive operations (delete, rename), always ask for confirmation first, "
                        "and only proceed after the user explicitly confirms with 'yes', 'confirm', or similar."
        )

        # Wait for the run to complete
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Handle tool calls if any
        tool_calls_made = []
        if run.status == "requires_action" and run.required_action.type == "submit_tool_outputs":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls

            tool_outputs = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the function based on the function name using MCP tools
                try:
                    if function_name == "add_task":
                        from .mcp_official_wrapper import mcp_official_wrapper
                        result = mcp_official_wrapper.handle_add_task(
                            session,
                            function_args["user_id"],
                            function_args["title"],
                            function_args.get("description")
                        )
                        output = result
                    elif function_name == "list_tasks":
                        from .mcp_official_wrapper import mcp_official_wrapper
                        result = mcp_official_wrapper.handle_list_tasks(
                            session,
                            function_args["user_id"],
                            function_args.get("status")
                        )
                        output = result
                    elif function_name == "complete_task":
                        from .mcp_official_wrapper import mcp_official_wrapper
                        result = mcp_official_wrapper.handle_complete_task(
                            session,
                            function_args["user_id"],
                            function_args["task_id"]
                        )
                        output = result
                    elif function_name == "delete_task":
                        from .mcp_official_wrapper import mcp_official_wrapper
                        result = mcp_official_wrapper.handle_delete_task(
                            session,
                            function_args["user_id"],
                            function_args["task_id"]
                        )
                        output = result
                    elif function_name == "update_task":
                        from .mcp_official_wrapper import mcp_official_wrapper
                        result = mcp_official_wrapper.handle_update_task(
                            session,
                            function_args["user_id"],
                            function_args["task_id"],
                            function_args.get("title"),
                            function_args.get("description")
                        )
                        output = result
                    else:
                        output = {"error": f"Unknown function: {function_name}"}

                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(output)
                    })

                    # Record the tool call that was made
                    tool_calls_made.append({
                        "name": function_name,
                        "arguments": function_args,
                        "result": output
                    })
                except Exception as e:
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps({"error": str(e)})
                    })

            # Submit the tool outputs
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            # Wait for the run to complete after tool outputs
            while run.status in ["queued", "in_progress"]:
                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Get the messages from the thread
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        # Extract the assistant's response (last message)
        response_text = "I processed your request."
        for msg in messages.data:
            if msg.role == "assistant":
                # Get the content of the message
                if msg.content and len(msg.content) > 0 and msg.content[0].type == "text":
                    response_text = msg.content[0].text.value
                    break

        return response_text, tool_calls_made
    except Exception as e:
        # If OpenAI API is not available, return a fallback response
        print(f"OpenAI API error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        response_text = f"I received your message: '{message}'. However, I'm unable to process it right now due to API configuration issues. The system is set up to use MCP tools for task management when the OpenAI API is available."
        return response_text, []
