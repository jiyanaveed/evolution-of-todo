# Phase 3: MCP Tools Specification

## Overview
This specification defines the Model Context Protocol (MCP) tools for the Todo AI Chatbot Phase 3. These tools implement the locked CRUD operations spec for Task entities.

## MCP Tools Interface

### 1. create_task
**Purpose**: Create a new task with the specified title
**Input Parameters**:
- `title` (string): Human-readable description of the task
- Authentication: User must be authenticated via JWT token

**Output**:
- Success: Object containing all task fields (id, title, completed, user_id)
- Error: Appropriate HTTP error code and message

**Behavior**:
- Creates a new task with `completed = false`
- Assigns the authenticated user's ID as the owner
- Validates that title is non-empty and contains non-whitespace characters

**Invariants Enforced**:
- New unique ID assigned to task
- Task owned by authenticated user
- Completion status starts as false

### 2. read_task
**Purpose**: Retrieve a specific task by ID
**Input Parameters**:
- `task_id` (integer): Unique identifier of the task to retrieve
- Authentication: User must be authenticated via JWT token

**Output**:
- Success: Task object with all fields (id, title, completed, user_id)
- Error: 404 if task not found or access denied, 403 if not owned by user

**Behavior**:
- Verifies that the task belongs to the authenticated user
- Returns complete task information if found and accessible

**Invariants Enforced**:
- Ownership validation before returning data
- No access to tasks owned by other users

### 3. update_task
**Purpose**: Update properties of an existing task
**Input Parameters**:
- `task_id` (integer): Unique identifier of the task to update
- `new_title` (string, optional): New title for the task
- `completed` (boolean, optional): New completion status
- Authentication: User must be authenticated via JWT token

**Output**:
- Success: Updated task object with all fields (id, title, completed, user_id)
- Error: Appropriate HTTP error code and message

**Behavior**:
- Modifies title if provided
- Modifies completion status if provided
- Enforces completion constraint (completed tasks cannot revert to incomplete)

**Invariants Enforced**:
- Ownership verification
- Completion constraint: can only change from false to true
- Title validation if being updated

### 4. delete_task
**Purpose**: Remove a task from the system
**Input Parameters**:
- `task_id` (integer): Unique identifier of the task to delete
- Authentication: User must be authenticated via JWT token

**Output**:
- Success: Confirmation message
- Error: 404 if task not found or access denied, 403 if not owned by user

**Behavior**:
- Removes the task from the database
- Verifies that the task belongs to the authenticated user

**Invariants Enforced**:
- Ownership verification before deletion
- Task ceases to exist after successful deletion

## Error Handling

### Authentication Errors
- 401 Unauthorized: Invalid or missing authentication token

### Authorization Errors
- 403 Forbidden: Attempting to access another user's tasks

### Validation Errors
- 400 Bad Request: Invalid input parameters (e.g., empty title)
- 400 Bad Request: Attempt to revert completed task to incomplete

### Resource Errors
- 404 Not Found: Task does not exist or access denied

### Server Errors
- 500 Internal Server Error: Unexpected server error

## Security Considerations
- All operations require valid JWT authentication
- Users can only access their own tasks
- Input validation applied to prevent injection attacks
- No information leakage between users

## Compliance with Locked Spec
- All domain invariants from the locked spec are enforced
- No additional fields or behaviors beyond the Task entity
- Strict adherence to completion constraint (false→true only)
- Ownership validation for all operations