# REST API Endpoints Specification

## Authentication Endpoints

### POST /auth/register
**Purpose**: Register a new user account
**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```
**Response**: UserResponse object with ID, email, and creation timestamp
**Status Codes**: 200 (success), 400 (email exists)

### POST /auth/login
**Purpose**: Authenticate user and return access token
**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```
**Response**: Token object with access_token and token_type
**Status Codes**: 200 (success), 401 (invalid credentials)

### GET /auth/me
**Purpose**: Get current user's information
**Headers**: Authorization: Bearer {token}
**Response**: UserResponse object
**Status Codes**: 200 (success), 401 (unauthorized)

## Task Management Endpoints

### GET /tasks
**Purpose**: Retrieve all tasks for the current user
**Headers**: Authorization: Bearer {token}
**Response**: Array of TaskResponse objects
**Status Codes**: 200 (success), 401 (unauthorized)

### POST /tasks
**Purpose**: Create a new task
**Headers**: Authorization: Bearer {token}
**Request Body**:
```json
{
  "title": "string"
}
```
**Response**: TaskResponse object
**Status Codes**: 201 (created), 401 (unauthorized)

### GET /tasks/{task_id}
**Purpose**: Retrieve a specific task
**Headers**: Authorization: Bearer {token}
**Path Parameter**: task_id (integer)
**Response**: TaskResponse object
**Status Codes**: 200 (success), 401 (unauthorized), 404 (not found)

### PUT /tasks/{task_id}
**Purpose**: Update an existing task
**Headers**: Authorization: Bearer {token}
**Path Parameter**: task_id (integer)
**Request Body**:
```json
{
  "title": "string",
  "completed": "boolean"
}
```
**Response**: TaskResponse object
**Status Codes**: 200 (success), 401 (unauthorized), 404 (not found), 422 (validation error)

### DELETE /tasks/{task_id}
**Purpose**: Delete a task
**Headers**: Authorization: Bearer {token}
**Path Parameter**: task_id (integer)
**Status Codes**: 204 (no content), 401 (unauthorized), 404 (not found)

### PATCH /tasks/{task_id}/complete
**Purpose**: Toggle task completion status
**Headers**: Authorization: Bearer {token}
**Path Parameter**: task_id (integer)
**Response**: TaskResponse object
**Status Codes**: 200 (success), 401 (unauthorized), 404 (not found)