"""
OpenAI Client for Phase 3 Todo AI Chatbot.
Provides LLM-powered intent recognition and response generation.
"""
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class OpenAIClient:
    """
    OpenAI client wrapper for the Todo AI Chatbot.
    Handles LLM interactions for intent recognition and response generation.
    """

    def __init__(self):
        self._client = None
        # Load from project root (one level up from backend directory) if not already set by system env
        import os
        from dotenv import load_dotenv
        if not os.getenv("OPENAI_API_KEY"):
            load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
        self._api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # System prompt for the todo assistant
        self.system_prompt = """You are a helpful todo list assistant. Your job is to help users manage their tasks through natural conversation.

Available operations:
1. CREATE a new task: "add [task title]", "create [task title]", "remind me to [task]"
2. READ tasks: "list my tasks", "show all tasks", "what do I have to do?"
3. UPDATE a task:
   - Complete a task: "complete task [id]", "finish [id]", "done with [id/title]", "complete [title]", "mark [title] as complete"
   - Rename a task: "rename task [id] to [new title]", "change [id] to [new title]", "update [title] to [new title]", "edit [title] to [new title]", "rename [title] to [new title]"
4. DELETE a task: "delete task [id]", "remove [id/title]"

TWO-STEP MUTATION RULE: For destructive operations (delete, rename/update), you must:
1. First ask for confirmation with the task details
2. Only proceed after user explicitly confirms with "yes", "yeah", "confirm", etc.

Task IDs are integers. When a user refers to a task by title without an ID, help them identify the correct task ID first.

Always be helpful, friendly, and concise in your responses."""

    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            if not self._api_key:
                from dotenv import load_dotenv
                import os
                # Load from project root (one level up from backend directory)
                load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
                self._api_key = os.getenv("OPENAI_API_KEY")
            if not self._api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            from openai import OpenAI
            self._client = OpenAI(api_key=self._api_key)
        return self._client

    def is_configured(self) -> bool:
        """Check if OpenAI is properly configured."""
        return bool(self._api_key)

    def chat(
        self,
        message: str,
        history: List[Dict[str, str]],
        tools_description: str = ""
    ) -> str:
        """
        Send a message to the LLM and get a response.

        Args:
            message: The user's current message
            history: List of previous messages in the conversation
            tools_description: Description of available tools (optional)

        Returns:
            The LLM's response
        """
        if not self.is_configured():
            raise RuntimeError("OpenAI is not configured. Set OPENAI_API_KEY in .env file.")

        # Build messages list
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history
        for msg in history:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

        # Add current message
        messages.append({"role": "user", "content": message})

        # Add tools description if provided
        if tools_description:
            messages.append({"role": "system", "content": f"Available tools:\n{tools_description}"})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def classify_intent(
        self,
        message: str,
        history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Classify the user's intent and extract entities.

        Args:
            message: The user's current message
            history: List of previous messages in the conversation

        Returns:
            Dictionary with intent and extracted entities
        """
        if not self.is_configured():
            raise RuntimeError("OpenAI is not configured. Set OPENAI_API_KEY in .env file.")

        prompt = f"""Analyze this todo assistant conversation and classify the intent.

Current message: "{message}"

History:
{chr(10).join([f"{m.get('role')}: {m.get('content', '')}" for m in history[-5:]])}

Intent classification guide:
- create: Adding a new task (keywords: add, create, new, remind me to)
- read: Listing tasks (keywords: list, show, all, my tasks)
- update_complete: Marking a task as complete (keywords: complete, finish, done, mark complete)
- update_rename: Renaming or updating a task title (keywords: update, rename, change, edit, when followed by "to" pattern like "[title] to [new_title]")
- delete: Deleting a task (keywords: delete, remove)
- confirm: User confirming a previous request (keywords: yes, confirm, sure, ok, yeah)

Respond with JSON (no markdown):
{{
    "intent": "create|read|update_complete|update_rename|delete|confirm|unknown",
    "task_id": null or integer,
    "task_title": null or string,
    "new_title": null or string,
    "needs_confirmation": boolean,
    "confirmation_message": null or string
}}"""

        messages = [
            {"role": "system", "content": "You are a todo assistant intent classifier. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=200
            )
            import json
            content = response.choices[0].message.content or "{}"
            # Clean up any markdown formatting
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            # Fallback to rule-based classification
            return {"intent": "unknown", "error": str(e)}


# Create client instance (lazy initialization)
def get_openai_client():
    return OpenAIClient()

# For backward compatibility, create instance when first accessed
_openai_client_instance = None
def __getattr__(name):
    global _openai_client_instance
    if name == "openai_client":
        if _openai_client_instance is None:
            _openai_client_instance = OpenAIClient()
        return _openai_client_instance
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
