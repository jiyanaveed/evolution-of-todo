"""
Agent Orchestration Layer for Phase 3 Todo AI Chatbot.
Implements the FETCH → APPEND → RUN → PERSIST → RESPOND lifecycle.
Uses OpenAI for intent recognition and response generation.
"""

from typing import List, Dict, Any, Optional
from sqlmodel import Session
from . import crud
from .mcp_official_wrapper import mcp_official_wrapper as mcp_server
from .agents_sdk import run_todo_agent
from .openai_client import openai_client
import uuid
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class AgentOrchestrator:
    """
    Orchestrates the conversation flow between the user and the MCP tools.
    Uses OpenAI for intelligent intent recognition and response generation.
    Strictly follows the Phase 3 Agent Behavior Specification.
    """

    def __init__(self, session: Session):
        self.session = session

    def handle_message(self, user_id: str, conversation_id: str, message_text: str) -> str:
        """
        Main orchestration loop: FETCH → APPEND → RUN → PERSIST → RESPOND.
        """
        # Convert conversation_id string back to integer for database operations
        try:
            conv_id_int = int(conversation_id)
        except (ValueError, TypeError):
            return "Error: Invalid conversation ID provided."

        # 1. FETCH: Retrieve unsummarized conversation history from DB
        history = crud.get_messages(self.session, conv_id_int, user_id)
        history_dicts = [
            {"role": m.role, "content": m.content}
            for m in history
        ]

        # 2. APPEND: The current user message is appended to the context for the model
        # (Implicitly handled by passing it along with history to the "RUN" phase)

        # 3. RUN: Use OpenAI for intent recognition and response generation
        response_text = self._orchestrate_llm_logic(
            user_id, conversation_id, message_text, history_dicts
        )

        # 4. PERSIST: Save both user input and agent response to DB
        crud.save_message(self.session, conv_id_int, user_id, "user", message_text)
        crud.save_message(self.session, conv_id_int, user_id, "assistant", response_text)

        # 5. RESPOND: Deliver the final NL response
        return response_text

    def _orchestrate_llm_logic(
        self, user_id: str, conversation_id: str, message_text: str, history: List[Dict[str, str]]
    ) -> str:
        """
        Uses OpenAI for intent recognition and generates appropriate responses.
        Enforces the Two-Step Mutation Rule for destructive operations.
        """
        # Get user's tasks for ID mapping (user-friendly 1-based IDs)
        user_tasks = crud.get_tasks_by_user(self.session, user_id)

        # Create mapping from user-friendly ID to database ID
        id_mapping = {i+1: t.id for i, t in enumerate(user_tasks)}
        # And reverse mapping for easy lookup
        db_to_user_id = {t.id: i+1 for i, t in enumerate(user_tasks)}

        # Check for pending confirmation from history (handles multi-turn confirmation flows)
        confirmation_result = self._check_for_confirmation(history, message_text, user_tasks)
        if confirmation_result:
            return confirmation_result

        # Use OpenAI for intent classification with enhanced context
        try:
            intent_data = openai_client.classify_intent(message_text, history)
            logger.info(f"OpenAI intent classification successful: {intent_data.get('intent')}")
        except RuntimeError as e:
            # Fallback to rule-based parsing if OpenAI fails
            logger.warning(f"OpenAI intent classification failed, using fallback: {e}")
            return self._fallback_logic(message_text, history, user_id, user_tasks, id_mapping)

        # Extract intent and entities from OpenAI response
        intent = intent_data.get("intent", "unknown")
        task_id = intent_data.get("task_id")
        task_title = intent_data.get("task_title")
        new_title = intent_data.get("new_title")
        needs_confirmation = intent_data.get("needs_confirmation", False)

        # Handle based on intent with enhanced logic
        if intent == "create":
            return self._handle_create_intent(task_title, message_text, user_id)

        elif intent == "read":
            return self._handle_read_intent(user_tasks)

        elif intent == "delete":
            return self._handle_delete_intent(
                task_id, task_title, user_tasks, db_to_user_id, needs_confirmation, user_id
            )

        elif intent == "update_rename":
            # If OpenAI didn't provide task_id or task_title but we have "to" in the message,
            # try to parse it from the message text
            if not task_id and not task_title and new_title and " to " in message_text.lower():
                # Try to extract task title from message
                parts = message_text.lower().rsplit(" to ", 1)
                if len(parts) == 2:
                    before_to = parts[0].strip()
                    # Remove update/rename/change prefixes
                    old_title = re.sub(r"^(?:update|rename|change|edit)\s+(?:task\s+)?", "", before_to).strip()
                    # Find the task by title
                    matching_task = next((t for t in user_tasks if t.title.lower() == old_title.lower()), None)
                    if matching_task:
                        task_id = matching_task.id
                        task_title = matching_task.title

            return self._handle_rename_intent(
                task_id, task_title, new_title, user_tasks, db_to_user_id, needs_confirmation, user_id
            )

        elif intent == "update_complete":
            return self._handle_complete_intent(
                task_id, task_title, user_tasks, db_to_user_id, user_id
            )

        elif intent == "confirm":
            # Already handled by confirmation check at the top
            return "I've processed your confirmation."

        elif intent == "unknown":
            # Before defaulting to general chat, try rule-based parsing for common operations
            # This handles cases where OpenAI doesn't recognize the intent but it's a clear task operation
            fallback_result = self._fallback_logic(message_text, history, user_id, user_tasks, id_mapping)
            # If fallback logic returns a specific task operation result, use it
            if fallback_result and not fallback_result.startswith("I'm sorry"):
                return fallback_result

            # Use full chat with OpenAI for general queries
            try:
                response = openai_client.chat(message_text, history)
                logger.info("OpenAI chat response generated successfully")
                return response
            except RuntimeError as e:
                logger.warning(f"OpenAI chat failed, using fallback: {e}")
                return self._fallback_logic(message_text, history, user_id, user_tasks, id_mapping)

        # Default response if intent is not recognized
        return "I'm sorry, I didn't quite catch that. You can ask me to add, list, complete, rename, or delete tasks."

    def _check_for_confirmation(self, history: List[Dict[str, str]], message_text: str, user_tasks: List) -> Optional[str]:
        """
        Check if the current message is a confirmation for a previous destructive operation.
        Enhanced to properly track conversation context and task information.
        Returns response if confirmation is detected, None otherwise.
        """
        if not history:
            return None

        # Find the last assistant message that requested confirmation
        last_assistant_msg = None
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                last_assistant_msg = msg
                break

        if not last_assistant_msg:
            return None

        # Check if last assistant message was a confirmation request
        content_lower = last_assistant_msg.get("content", "").lower()
        is_confirmation_request = (
            "are you sure" in content_lower or
            "confirm" in content_lower or
            "delete" in content_lower or
            "rename" in content_lower or
            "update" in content_lower or
            "yes" in content_lower or
            "to proceed" in content_lower or
            "please confirm" in content_lower
        )

        if not is_confirmation_request:
            return None

        # Check if current user message is affirmative
        msg_lower = message_text.lower().strip()
        is_affirmative = msg_lower in ["yes", "yeah", "yep", "confirm", "do it", "sure", "okay", "ok", "y", "confirmed"]

        if not is_affirmative:
            return None  # Not a confirmation, continue normal processing

        # Look for task information in the assistant's confirmation request
        import re

        # Create user-friendly ID mapping for proper lookup
        db_to_user_id = {t.id: i+1 for i, t in enumerate(user_tasks)}

        # Extract task ID or title from the assistant's confirmation request
        # Look for patterns like "task 1", "task 'title'", etc.
        task_id_match = re.search(r"task\s+(\d+)", last_assistant_msg.get("content", ""), re.IGNORECASE)
        task_title_match = re.search(r"task\s+'([^']+)'|task\s+\"([^\"]+)\"", last_assistant_msg.get("content", ""), re.IGNORECASE)

        # Find the original user command that triggered the confirmation
        original_command = None
        for msg in reversed(history):
            if msg.get("role") == "user":
                original_command = msg.get("content", "")
                break

        if not original_command:
            return "I couldn't find the original request to process your confirmation. Please try the command again."

        # Determine operation type from original command
        original_lower = original_command.lower()

        if "delete" in original_lower or "remove" in original_lower:
            if task_id_match:
                requested_user_id = int(task_id_match.group(1))

                # Find the actual database ID that corresponds to the user-friendly ID
                target_task = next((t for t in user_tasks if db_to_user_id[t.id] == requested_user_id), None)

                if target_task:
                    result = mcp_server.handle_delete_task(self.session, target_task.user_id, target_task.id)
                    return f"Task '{target_task.title}' has been deleted."
                else:
                    return "Task not found. Could not process deletion."
            elif task_title_match:
                title = task_title_match.group(1) or task_title_match.group(2)
                target_task = next((t for t in user_tasks if t.title.lower() == title.lower()), None)
                if target_task:
                    result = mcp_server.handle_delete_task(self.session, target_task.user_id, target_task.id)
                    return f"Task '{target_task.title}' has been deleted."
                else:
                    return "Task not found. Could not process deletion."
            else:
                return "Could not determine task for deletion operation."

        elif "rename" in original_lower or "update" in original_lower or "change" in original_lower:
            if task_id_match:
                requested_user_id = int(task_id_match.group(1))

                # Find the actual database ID that corresponds to the user-friendly ID
                target_task = next((t for t in user_tasks if db_to_user_id[t.id] == requested_user_id), None)

                if not target_task:
                    return "Task not found. Could not process update."

                # Extract new title from original command - more flexible pattern matching
                # Pattern: "update/rename [old_title] to [new_title]" or similar variations
                update_patterns = [
                    r"(?:update|rename|change)\s+(?:task\s+\d+\s+)?(?:['\"]?)([^'\"]+)(?:['\"]?)\s+to\s+(.+)",
                    r"(?:update|rename|change)\s+(?:task\s+\d+\s+)?(.+?)\s+to\s+(.+)",
                    r"(?:update|rename|change)\s+(?:task\s+)?(.+?)\s+to\s+(.+)"
                ]

                new_title = None
                for pattern in update_patterns:
                    update_match = re.search(pattern, original_command, re.IGNORECASE)
                    if update_match:
                        new_title = update_match.group(2).strip().strip('"\'""')
                        break

                if new_title:
                    result = mcp_server.handle_update_task(
                        self.session, target_task.user_id, target_task.id, title=new_title
                    )
                    return f"Task '{target_task.title}' has been renamed to '{new_title}'."
                else:
                    return "Could not determine new title for update operation."

            elif task_title_match:
                title = task_title_match.group(1) or task_title_match.group(2)
                # Extract new title from original command - more flexible pattern matching
                update_patterns = [
                    r"(?:update|rename|change)\s+(?:task\s+)?(?:['\"]?)" + re.escape(title) + r"(?:['\"]?)\s+to\s+(.+)",
                    r"(?:update|rename|change)\s+(?:task\s+)?(.+?)\s+to\s+(.+)",
                    r"(?:update|rename|change)\s+(.+?)\s+to\s+(.+)"
                ]

                new_title = None
                for pattern in update_patterns:
                    update_match = re.search(pattern, original_command, re.IGNORECASE)
                    if update_match:
                        new_title = update_match.group(2).strip().strip('"\'""')
                        break

                if not new_title:
                    # Try to extract new title from after the "to" part in the original command
                    parts = original_command.rsplit(" to ", 1)
                    if len(parts) == 2:
                        new_title = parts[1].strip().strip('"\'""')

                if new_title:
                    # Find the task by title
                    target_task = next((t for t in user_tasks if t.title.lower() == title.lower()), None)
                    if target_task:
                        result = mcp_server.handle_update_task(
                            self.session, target_task.user_id, target_task.id, title=new_title
                        )
                        return f"Task '{target_task.title}' has been renamed to '{new_title}'."
                    else:
                        return "Task not found. Could not process update."
                else:
                    return "Could not determine new title for update operation."
            else:
                return "Could not determine task for update operation."

        return "Processed your confirmation."

    def _process_confirmation(self, history: List[Dict[str, str]], last_assistant_msg: Dict, message_text: str, user_tasks: List) -> str:
        """
        Process a confirmed destructive operation based on the original request.
        """
        import re

        # Extract task ID from confirmation prompt
        match = re.search(r"task\s*(\d+)", last_assistant_msg.get("content", ""))
        if not match:
            return "I couldn't process your confirmation. Please try the command again."

        user_task_id = int(match.group(1))

        # Find the task to operate on by user-friendly ID
        target_task = next((t for t in user_tasks if t.id == user_task_id), None)
        if not target_task:
            return "Task not found. Could not process confirmation."

        # Find the original user request before the confirmation prompt
        original_message = None
        for msg in reversed(history):
            if msg.get("role") == "user":
                original_message = msg.get("content", "")
                break

        if not original_message:
            return "I couldn't find the original request. Please try again."

        # Determine the operation type from the original message
        original_lower = original_message.lower()

        if "delete" in original_lower or "remove" in original_lower:
            result = mcp_server.handle_delete_task(self.session, target_task.user_id, target_task.id)
            return f"Task '{target_task.title}' has been deleted."

        elif "rename" in original_lower or "change" in original_lower or "update" in original_lower:
            # Extract new title from original message for rename operations
            rename_match = re.search(
                r"(?:rename|change|update).*?(?:task\s*\d+)?\s*(?:to\s*|=)\s*(.+)", original_message
            )
            if rename_match:
                new_title = rename_match.group(1).strip().strip('"\'""')
                result = mcp_server.handle_update_task(
                    self.session, target_task.user_id, target_task.id, title=new_title
                )
                return f"Task '{target_task.title}' has been renamed to '{new_title}'."
            else:
                return "Could not determine new title for rename operation."

        return "Processed your confirmation."

    def _handle_create_intent(self, task_title: Optional[str], message_text: str, user_id: str) -> str:
        """
        Handle task creation intent with proper title extraction.
        """
        title = task_title or message_text
        # Extract title from message if not classified
        if not task_title:
            for prefix in ["add ", "create ", "remind me to ", "new task: ", "please add "]:
                if title.lower().startswith(prefix):
                    title = title[len(prefix):].strip()
                    break

        if title:
            result = mcp_server.handle_add_task(self.session, user_id, title.strip(), None)
            return f"Task '{title.strip()}' has been added to your list."
        else:
            return "What would you like to add to your todo list?"

    def _handle_read_intent(self, user_tasks: List) -> str:
        """
        Handle task listing intent with proper formatting.
        """
        if not user_tasks:
            return "You have no tasks in your list."

        # Format task list with user-friendly numbering
        task_list = "\n".join([
            f"{i+1}. {t.title} [{'x' if t.completed else ' '}]"
            for i, t in enumerate(user_tasks)
        ])
        return f"Here are your tasks:\n{task_list}"

    def _handle_delete_intent(
        self, task_id: Optional[int], task_title: Optional[str], user_tasks: List,
        db_to_user_id: Dict, needs_confirmation: bool, user_id: str
    ) -> str:
        """
        Handle task deletion with proper confirmation and error handling.
        """
        if task_id:
            # Convert database ID to user-friendly ID for display
            user_friendly_id = db_to_user_id.get(task_id, task_id)
            existing_task = next((t for t in user_tasks if t.id == task_id), None)

            if existing_task:
                if needs_confirmation:
                    return f"Are you sure you want to delete task {user_friendly_id} ('{existing_task.title}')? Please confirm with 'yes' to proceed."
                else:
                    result = mcp_server.handle_delete_task(self.session, user_id, task_id)
                    return f"Task '{existing_task.title}' has been deleted."
            else:
                return f"Task {user_friendly_id} not found. Use 'list my tasks' to see available tasks."
        else:
            # Try to find task by title if no ID provided
            if task_title:
                matching_tasks = [t for t in user_tasks if task_title.lower() in t.title.lower()]
                if len(matching_tasks) == 1:
                    task = matching_tasks[0]
                    user_friendly_id = db_to_user_id[task.id]
                    if needs_confirmation:
                        return f"Are you sure you want to delete task {user_friendly_id} ('{task.title}')? Please confirm with 'yes' to proceed."
                    else:
                        result = mcp_server.handle_delete_task(self.session, user_id, task.id)
                        return f"Task '{task.title}' has been deleted."
                elif len(matching_tasks) > 1:
                    task_list = ", ".join([f"'{t.title}'" for t in matching_tasks])
                    return f"Multiple tasks match '{task_title}': {task_list}. Please specify by number or exact title."
                else:
                    return f"No tasks found matching '{task_title}'. Use 'list my tasks' to see available tasks."

            return "Which task would you like to delete? Please provide the task ID or title."

    def _handle_rename_intent(
        self, task_id: Optional[int], task_title: Optional[str], new_title: Optional[str],
        user_tasks: List, db_to_user_id: Dict, needs_confirmation: bool, user_id: str
    ) -> str:
        """
        Handle task renaming with proper validation and confirmation.
        Enhanced to handle partial title matches and better error reporting.
        """
        if task_id and new_title:
            user_friendly_id = db_to_user_id.get(task_id, task_id)
            existing_task = next((t for t in user_tasks if t.id == task_id), None)

            if existing_task:
                if needs_confirmation:
                    return f"Are you sure you want to rename task {user_friendly_id} ('{existing_task.title}') to '{new_title}'? Please confirm with 'yes' to proceed."
                else:
                    result = mcp_server.handle_update_task(
                        self.session, user_id, task_id, title=new_title
                    )
                    return f"Task '{existing_task.title}' has been successfully updated to '{new_title}'."
            else:
                return f"Task with ID {task_id} not found. Use 'list my tasks' to see available tasks."
        elif task_title and new_title:
            # Find task by exact title match first, then partial match
            exact_match = next((t for t in user_tasks if t.title.lower() == task_title.lower()), None)
            if exact_match:
                user_friendly_id = db_to_user_id[exact_match.id]
                if needs_confirmation:
                    return f"Are you sure you want to rename task {user_friendly_id} ('{exact_match.title}') to '{new_title}'? Please confirm with 'yes' to proceed."
                else:
                    result = mcp_server.handle_update_task(
                        self.session, user_id, exact_match.id, title=new_title
                    )
                    return f"Task '{exact_match.title}' has been successfully updated to '{new_title}'."

            # If no exact match, try partial match
            partial_matches = [t for t in user_tasks if task_title.lower() in t.title.lower()]
            if len(partial_matches) == 1:
                task = partial_matches[0]
                user_friendly_id = db_to_user_id[task.id]
                if needs_confirmation:
                    return f"Are you sure you want to rename task {user_friendly_id} ('{task.title}') to '{new_title}'? Please confirm with 'yes' to proceed."
                else:
                    result = mcp_server.handle_update_task(
                        self.session, user_id, task.id, title=new_title
                    )
                    return f"Task '{task.title}' has been successfully updated to '{new_title}'."
            elif len(partial_matches) > 1:
                task_list = ", ".join([f"'{t.title}' (ID: {db_to_user_id[t.id]})" for t in partial_matches])
                return f"Multiple tasks match '{task_title}': {task_list}. Please specify by number or exact title."
            else:
                # Try to find by looking for the longest matching substring
                for t in user_tasks:
                    if task_title.lower() in t.title.lower() or t.title.lower() in task_title.lower():
                        user_friendly_id = db_to_user_id[t.id]
                        if needs_confirmation:
                            return f"Are you sure you want to rename task {user_friendly_id} ('{t.title}') to '{new_title}'? Please confirm with 'yes' to proceed."
                        else:
                            result = mcp_server.handle_update_task(
                                self.session, user_id, t.id, title=new_title
                            )
                            return f"Task '{t.title}' has been successfully updated to '{new_title}'."

                return f"No tasks found matching '{task_title}'. Use 'list my tasks' to see available tasks."

        return "Please specify which task to rename and the new title."

    def _handle_complete_intent(
        self, task_id: Optional[int], task_title: Optional[str], user_tasks: List,
        db_to_user_id: Dict, user_id: str
    ) -> str:
        """
        Handle task completion with proper validation and response.
        Enhanced to handle partial title matches and better error reporting.
        """
        if task_id:
            user_friendly_id = db_to_user_id.get(task_id, task_id)
            existing_task = next((t for t in user_tasks if t.id == task_id), None)

            if existing_task:
                if existing_task.completed:
                    return f"Task {user_friendly_id} ('{existing_task.title}') is already completed."
                else:
                    result = mcp_server.handle_complete_task(
                        self.session, user_id, task_id
                    )
                    return f"Task '{existing_task.title}' has been successfully marked as completed."
            else:
                return f"Task with ID {task_id} not found. Use 'list my tasks' to see available tasks."
        elif task_title:
            # Find task by exact title match first
            exact_match = next((t for t in user_tasks if t.title.lower() == task_title.lower()), None)
            if exact_match:
                user_friendly_id = db_to_user_id[exact_match.id]
                if exact_match.completed:
                    return f"Task '{exact_match.title}' is already completed."
                else:
                    result = mcp_server.handle_complete_task(
                        self.session, user_id, exact_match.id
                    )
                    return f"Task '{exact_match.title}' has been successfully marked as completed."

            # If no exact match, try partial match
            partial_matches = [t for t in user_tasks if task_title.lower() in t.title.lower()]
            if len(partial_matches) == 1:
                task = partial_matches[0]
                if task.completed:
                    return f"Task '{task.title}' is already completed."
                else:
                    result = mcp_server.handle_complete_task(
                        self.session, user_id, task.id
                    )
                    return f"Task '{task.title}' has been successfully marked as completed."
            elif len(partial_matches) > 1:
                task_list = ", ".join([f"'{t.title}' (ID: {db_to_user_id[t.id]})" for t in partial_matches])
                return f"Multiple tasks match '{task_title}': {task_list}. Please specify by number or exact title."
            else:
                # Try to find by looking for the longest matching substring
                for t in user_tasks:
                    if task_title.lower() in t.title.lower() or t.title.lower() in task_title.lower():
                        if t.completed:
                            return f"Task '{t.title}' is already completed."
                        else:
                            result = mcp_server.handle_complete_task(
                                self.session, user_id, t.id
                            )
                            return f"Task '{t.title}' has been successfully marked as completed."

                return f"No tasks found matching '{task_title}'. Use 'list my tasks' to see available tasks."

        return "Which task would you like to complete? Please provide the task ID or title."

    def _fallback_logic(
        self, message_text: str, history: List[Dict[str, str]], user_id: str,
        user_tasks: List, id_mapping: Dict
    ) -> str:
        """
        Fallback rule-based logic when OpenAI is unavailable.
        Enhanced with better task lookup, natural language processing, and error handling.
        """
        msg_lower = message_text.lower().strip()

        # Check for pending confirmation first
        confirmation_result = self._check_for_confirmation(history, message_text, user_tasks)
        if confirmation_result:
            return confirmation_result

        import re

        # CREATE Intent - Check first to avoid confusion with other operations
        if any(keyword in msg_lower for keyword in ["add", "remind me", "create", "new task"]):
            # Extract title after keywords
            title = None
            for prefix in ["add ", "remind me to ", "create ", "new task: ", "please add "]:
                if prefix in msg_lower:
                    title = message_text[msg_lower.find(prefix) + len(prefix):].strip()
                    break

            if not title:
                # If no recognized prefix, check if it looks like a simple task addition
                # Avoid catching update patterns by checking for ' to ' first
                if " to " not in msg_lower:
                    title = message_text.strip()

            if title and title.lower() not in ["add", "create", "new task", "remind me"]:
                result = mcp_server.handle_add_task(self.session, user_id, title, None)
                return f"Task '{title}' has been added to your list."
            return "What would you like to add to your todo list?"

        # UPDATE/Rename Intent - Handle patterns like "update buy prop to sleep", "edit buy prop to buy water", etc.
        if " to " in msg_lower:
            # Handle patterns like "update [task_title] to [new_title]", "rename [task_title] to [new_title]",
            # "change [task_title] to [new_title]", "edit [task_title] to [new_title]", or just "[old_title] to [new_title]"

            # Split at the LAST " to " to get old_title and new_title (handles cases where new title contains " to ")
            parts = msg_lower.rsplit(" to ", 1)
            if len(parts) == 2:
                before_to = parts[0].strip()
                new_title = parts[1].strip().strip('"\'""')

                # Extract old title from before_to (remove prefixes like "update", "rename", "change", "edit", "task")
                old_title = re.sub(r"^(?:update|rename|change|edit)\s+(?:task\s+)?", "", before_to).strip()

                # Special case: if the old title is just a number, treat it as a task ID
                if old_title.isdigit():
                    task_id = int(old_title)
                    db_task_id = id_mapping.get(task_id)
                    if db_task_id:
                        # Find the task object to get the current title
                        target_task = next((t for t in user_tasks if t.id == db_task_id), None)
                        if target_task:
                            result = mcp_server.handle_update_task(
                                self.session, user_id, db_task_id, title=new_title
                            )
                            return f"Task '{target_task.title}' has been successfully updated to '{new_title}'."
                        else:
                            return f"Task with ID {task_id} not found. Use 'list my tasks' to see available tasks."

                # Find task by exact title match first
                exact_match = next((t for t in user_tasks if t.title.lower() == old_title.lower()), None)
                if exact_match:
                    result = mcp_server.handle_update_task(
                        self.session, user_id, exact_match.id, title=new_title
                    )
                    return f"Task '{exact_match.title}' has been successfully updated to '{new_title}'."

                # If no exact match, try partial match (case-insensitive substring)
                partial_matches = [t for t in user_tasks if old_title.lower() in t.title.lower()]
                if len(partial_matches) == 1:
                    task = partial_matches[0]
                    result = mcp_server.handle_update_task(
                        self.session, user_id, task.id, title=new_title
                    )
                    return f"Task '{task.title}' has been successfully updated to '{new_title}'."
                elif len(partial_matches) > 1:
                    task_list = ", ".join([f"'{t.title}' (ID: {next(k for k, v in id_mapping.items() if v == t.id)})" for t in partial_matches])
                    return f"Multiple tasks match '{old_title}': {task_list}. Please specify by number or exact title."
                else:
                    # Try broader matching (titles that contain the old_title or vice versa)
                    for t in user_tasks:
                        if old_title.lower() in t.title.lower() or t.title.lower() in old_title.lower():
                            result = mcp_server.handle_update_task(
                                self.session, user_id, t.id, title=new_title
                            )
                            return f"Task '{t.title}' has been successfully updated to '{new_title}'."

                    # If still no match, try with the original before_to (in case prefixes weren't removed properly)
                    original_old_title = before_to.strip()
                    if original_old_title != old_title:
                        exact_match = next((t for t in user_tasks if t.title.lower() == original_old_title.lower()), None)
                        if exact_match:
                            result = mcp_server.handle_update_task(
                                self.session, exact_match.id, user_id, new_title=new_title
                            )
                            return f"Task '{exact_match.title}' has been successfully updated to '{new_title}'."

                        partial_matches = [t for t in user_tasks if original_old_title.lower() in t.title.lower()]
                        if len(partial_matches) == 1:
                            task = partial_matches[0]
                            result = mcp_server.handle_update_task(
                                self.session, task.id, user_id, new_title=new_title
                            )
                            return f"Task '{task.title}' has been successfully updated to '{new_title}'."

                    return f"No tasks found matching '{old_title}'. Use 'list my tasks' to see available tasks."

        # COMPLETE Intent - Handle patterns like "mark complete to do shopping", "complete do shopping", etc.
        if any(keyword in msg_lower for keyword in ["complete", "finish", "done", "mark complete"]):
            # Handle "complete task [ID]" pattern
            complete_task_pattern = re.search(r"complete\s+task\s+(\d+)", msg_lower)
            if complete_task_pattern:
                task_num = int(complete_task_pattern.group(1))
                db_task_id = id_mapping.get(task_num)
                if db_task_id:
                    # Find the task to get its title
                    matching_task = next((t for t in user_tasks if t.id == db_task_id), None)
                    if matching_task:
                        result = mcp_server.handle_complete_task(
                            self.session, user_id, db_task_id
                        )
                        return f"Task '{matching_task.title}' has been successfully marked as completed."
                    else:
                        return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."
                else:
                    return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."

            # If no ID pattern matched, look for task title
            # Look for specific task title after completion keywords
            completion_keywords = ["complete ", "finish ", "done ", "mark complete "]
            for keyword in completion_keywords:
                if keyword in msg_lower:
                    # Extract the task title part after the keyword
                    title_part = msg_lower.split(keyword, 1)[1].strip()
                    if title_part:
                        # Find task by exact title match first
                        exact_match = next((t for t in user_tasks if t.title.lower() == title_part.lower()), None)
                        if exact_match:
                            result = mcp_server.handle_complete_task(
                                self.session, user_id, exact_match.id
                            )
                            return f"Task '{exact_match.title}' has been successfully marked as completed."

                        # If no exact match, try partial match
                        partial_matches = [t for t in user_tasks if title_part.lower() in t.title.lower()]
                        if len(partial_matches) == 1:
                            task = partial_matches[0]
                            result = mcp_server.handle_complete_task(
                                self.session, user_id, task.id
                            )
                            return f"Task '{task.title}' has been successfully marked as completed."
                        elif len(partial_matches) > 1:
                            task_list = ", ".join([f"'{t.title}'" for t in partial_matches])
                            return f"Multiple tasks match '{title_part}': {task_list}. Please specify by number or exact title."
                        else:
                            # Try more flexible matching (titles that contain the title_part or vice versa)
                            for t in user_tasks:
                                if title_part.lower() in t.title.lower() or t.title.lower() in title_part.lower():
                                    result = mcp_server.handle_complete_task(
                                        self.session, user_id, t.id
                                    )
                                    return f"Task '{t.title}' has been successfully marked as completed."

                    break  # Process only the first match

            # If no title part found, look for ID mentioned without "task" keyword
            id_match = re.search(r"complete\s+(\d+)", msg_lower)
            if id_match:
                task_num = int(id_match.group(1))
                db_task_id = id_mapping.get(task_num)
                if db_task_id:
                    # Find the task to get its title
                    matching_task = next((t for t in user_tasks if t.id == db_task_id), None)
                    if matching_task:
                        result = mcp_server.handle_complete_task(
                            self.session, user_id, db_task_id
                        )
                        return f"Task '{matching_task.title}' has been successfully marked as completed."
                    else:
                        return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."
                else:
                    return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."

            # If still no match, try to extract a potential title from the message
            # Remove completion keywords and see if what's left might be a task title
            remaining_text = msg_lower
            for keyword in completion_keywords:
                if keyword in remaining_text:
                    remaining_text = remaining_text.split(keyword, 1)[1].strip()
                    break

            if remaining_text and remaining_text not in ["it", "that", "the task"]:
                # Try exact match
                exact_match = next((t for t in user_tasks if t.title.lower() == remaining_text), None)
                if exact_match:
                    result = mcp_server.handle_update_task(
                        self.session, exact_match.id, user_id, completed=True
                    )
                    return f"Task '{exact_match.title}' has been successfully marked as completed."

                # Try partial match
                partial_matches = [t for t in user_tasks if remaining_text in t.title.lower()]
                if len(partial_matches) == 1:
                    task = partial_matches[0]
                    result = mcp_server.handle_update_task(
                        self.session, task.id, user_id, completed=True
                    )
                    return f"Task '{task.title}' has been successfully marked as completed."

            return "Which task would you like to complete? Please provide the task title or number."

        # DELETE Intent - Enhanced with better ID extraction
        if any(keyword in msg_lower for keyword in ["delete", "remove"]):
            # Handle "delete task [ID]" pattern
            delete_task_pattern = re.search(r"delete\s+task\s+(\d+)", msg_lower)
            if delete_task_pattern:
                task_num = int(delete_task_pattern.group(1))
                db_task_id = id_mapping.get(task_num)
                if db_task_id:
                    # Find the task to get its title
                    matching_task = next((t for t in user_tasks if t.id == db_task_id), None)
                    if matching_task:
                        return f"Are you sure you want to delete task {task_num} ('{matching_task.title}')? Please confirm with 'yes' to proceed."
                    else:
                        return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."
                else:
                    return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."

            # Try to extract task ID from message without "task" keyword
            id_match = re.search(r"(?:delete|remove)\s+(\d+)", msg_lower)
            if id_match:
                task_num = int(id_match.group(1))
                db_task_id = id_mapping.get(task_num)
                if db_task_id:
                    # Find the task to get its title
                    matching_task = next((t for t in user_tasks if t.id == db_task_id), None)
                    if matching_task:
                        return f"Are you sure you want to delete task {task_num} ('{matching_task.title}')? Please confirm with 'yes' to proceed."
                    else:
                        return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."
                else:
                    return f"Task with ID {task_num} not found. Use 'list my tasks' to see available tasks."

            # Try to find by title if no ID found
            delete_keywords = ["delete ", "remove "]
            for keyword in delete_keywords:
                if keyword in msg_lower:
                    title_part = msg_lower.split(keyword, 1)[1].strip()
                    if title_part:
                        # Find task by exact title match first
                        exact_match = next((t for t in user_tasks if t.title.lower() == title_part.lower()), None)
                        if exact_match:
                            user_friendly_id = next(k for k, v in id_mapping.items() if v == exact_match.id)
                            return f"Are you sure you want to delete task {user_friendly_id} ('{exact_match.title}')? Please confirm with 'yes' to proceed."

                        # If no exact match, try partial match
                        matching_tasks = [t for t in user_tasks if title_part.lower() in t.title.lower()]
                        if len(matching_tasks) == 1:
                            user_friendly_id = next(k for k, v in id_mapping.items() if v == matching_tasks[0].id)
                            return f"Are you sure you want to delete task {user_friendly_id} ('{matching_tasks[0].title}')? Please confirm with 'yes' to proceed."
                        elif len(matching_tasks) > 1:
                            task_list = ", ".join([f"'{t.title}'" for t in matching_tasks])
                            return f"Multiple tasks match '{title_part}': {task_list}. Please specify by number or exact title."
                        else:
                            # Try broader matching
                            for t in user_tasks:
                                if title_part.lower() in t.title.lower() or t.title.lower() in title_part.lower():
                                    user_friendly_id = next(k for k, v in id_mapping.items() if v == t.id)
                                    return f"Are you sure you want to delete task {user_friendly_id} ('{t.title}')? Please confirm with 'yes' to proceed."

                    break  # Process only the first match

            # If still no match, try to extract a potential title from the message
            # Remove delete keywords and see if what's left might be a task title
            remaining_text = msg_lower
            for keyword in delete_keywords:
                if keyword in remaining_text:
                    remaining_text = remaining_text.split(keyword, 1)[1].strip()
                    break

            if remaining_text and remaining_text not in ["it", "that", "the task"]:
                # Try exact match
                exact_match = next((t for t in user_tasks if t.title.lower() == remaining_text), None)
                if exact_match:
                    user_friendly_id = next(k for k, v in id_mapping.items() if v == exact_match.id)
                    return f"Are you sure you want to delete task {user_friendly_id} ('{exact_match.title}')? Please confirm with 'yes' to proceed."

                # Try partial match
                partial_matches = [t for t in user_tasks if remaining_text in t.title.lower()]
                if len(partial_matches) == 1:
                    user_friendly_id = next(k for k, v in id_mapping.items() if v == partial_matches[0].id)
                    return f"Are you sure you want to delete task {user_friendly_id} ('{partial_matches[0].title}')? Please confirm with 'yes' to proceed."

            return "Please specify which task to delete by number or title."

        # LIST Intent - Enhanced task listing
        if any(keyword in msg_lower for keyword in ["list", "show", "my tasks", "all tasks"]):
            if not user_tasks:
                return "You have no tasks in your list."

            task_list = "\n".join([
                f"{i+1}. {t.title} [{'x' if t.completed else ' '}]"
                for i, t in enumerate(user_tasks)
            ])
            return f"Here are your tasks:\n{task_list}"

        return "I'm sorry, I didn't quite catch that. You can ask me to add, list, complete, rename, or delete tasks."