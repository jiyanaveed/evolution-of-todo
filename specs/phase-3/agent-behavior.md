# Agent Behavior Specification - Phase 3

## Overview
This specification defines the behavior of the AI Agent in Phase 3 of "The Evolution of Todo". The agent serves as a natural language interface layered above the existing MCP tools. It is responsible for orchestrating the flow between user input, tool execution, and response generation while maintaining stateless execution via database persistence.

## LLM Provider

Phase 3 uses **OpenAI** as the LLM provider for intent recognition and response generation via the OpenAI Assistants API.

### OpenAI Configuration
- **Model**: `gpt-4o-mini` (configurable via `OPENAI_MODEL` env var)
- **API Key**: Set via `OPENAI_API_KEY` environment variable
- **Features Used**:
  - OpenAI Assistants API with function calling for tool execution
  - Thread management for conversation context
  - Function tools for CRUD operations

### Fallback Behavior
If OpenAI API is unavailable or returns an error, the agent falls back to rule-based intent parsing. This ensures the chatbot remains functional even during API outages.

## Agent Constraints
1. **Tool-Only Access**: The agent MUST NOT access the database or task logic directly. All operations MUST go through MCP tools.
2. **Statelessness**: The agent does not hold state in memory. Conversation history and context must be retrieved from the database or passed in the context.
3. **Implicit Ownership**: Ownership and authentication are handled within the MCP tool layer; the agent passes the `user_id` context to the tools.
4. **Explicit Confirmation**: The agent MUST confirm any mutation (Create, Update, Delete, Toggle) to the user.
5. **No Hallucination**: The agent MUST only report task states returned by tools. If a tool fails, the agent reports the error provided by the system.
6. **Two-Step Mutation Rule (LOCKED)**:
   For Delete and irreversible Update operations, the agent MUST:
   - Ask for explicit user confirmation if not already confirmed in the same message.
   - Proceed only after a clear affirmative response.
   - Create and Complete actions may execute immediately with post-action confirmation.

## Agent Decision Table (LOCKED)

| User Intent | MCP Tool | Required Parameters | Confirmation Behavior |
|-------------|----------|---------------------|-----------------------|
| Create: "Add...", "Remind me to..." | `create_todo_task` | `title` (string) | "Created task: [Title]" |
| Read: "Show task...", "Details for..." | `get_todo_task` | `task_id` (integer) | Display task details |
| List: "What's on my list?", "Show all" | `list_todo_tasks` | None | Display list of tasks |
| Update: "Rename task... to..." | `update_todo_task` | `task_id`, `title` (string) | "Are you sure you want to rename task [ID]? (yes/no)" |
| Complete: "Finish...", "Done with..." | `complete_todo_task`| `task_id` (integer) | "Completed task: [Title]" |
| Delete: "Delete...", "Remove task..." | `delete_todo_task` | `task_id` (integer) | "Are you sure you want to delete task [ID]? (yes/no)" |

## Conversation Lifecycle Rules (LOCKED)

1. **Conversation Identity**:
   - A `conversation_id` (UUIDv4) is generated at the start of a new session.
   - The same `conversation_id` is reused for all subsequent messages in that specific thread.
2. **Execution Sequence (Stateless)**:
   - **FETCH**: Retrieve full conversation history for the given `conversation_id` and `user_id` from the database.
   - **APPEND**: Append the current User message to the retrieved context.
   - **RUN**: Pass the context to the AI model to determine the next action (tool call or response).
   - **PERSIST**: Save both the user prompt and the final agent response (including tool results) back to the database.
   - **RESPOND**: Deliver the final NL response to the client.
3. **Prohibitions**:
   - **No Memory**: No in-memory caching of task state or intermediate variables across requests.
   - **No Summarization**: History must not be summarized; it remains an immutable log of messages.
   - **No Inferred State**: The agent must never assume a task was created or modified unless the MCP tool returns a successful confirmation.

## Message Execution Flow

1. **Input**: User sends Natural Language (NL) message.
2. **Context Retrieval**: System fetches recent conversation history from `messages` table.
3. **Intent Recognition**: Agent maps NL to one or more MCP tool calls using OpenAI Assistants API.
4. **Parameters Preparation**: Agent extracts required arguments from NL or history.
5. **Tool Execution**: Agent calls the Tool via the MCP protocol through OpenAI's function calling.
6. **Result Processing**:
    - **Success**: Agent generates NL confirmation based on tool output.
    - **Error**: Agent generates NL error explanation based on tool failure.
7. **Persistence**: The request and response are saved to the `messages` table.
8. **Output**: NL response returned to user.

## Agent Orchestration Implementation

The agent implementation uses OpenAI's Assistants API with the following workflow:

1. **Thread Creation**: A new thread is created for each conversation
2. **Message Addition**: User message is added to the thread
3. **Run Execution**: Assistant processes the message with configured tools
4. **Tool Calling**: When required, the assistant calls registered functions
5. **Result Submission**: Tool results are submitted back to the assistant
6. **Response Generation**: Final response is generated and returned to the user
