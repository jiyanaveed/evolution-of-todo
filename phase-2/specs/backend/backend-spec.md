# Phase 2 Backend Specification: Evolution of Todo

## Overview
This document specifies the backend implementation for Phase 2 of the Evolution of Todo application. The backend will be built using FastAPI, SQLModel, and Neon Postgres database to provide a robust REST API for task management.

## Database Models

### Task Model
The primary data model for the application representing a single task.

**Fields:**
- `id` (INTEGER): Primary key, auto-incrementing unique identifier
- `title` (VARCHAR/TEXT): Required task description, maximum 255 characters
- `completed` (BOOLEAN): Task completion status, defaults to `false`

**Constraints:**
- `id` is the primary key
- `title` is required (NOT NULL)
- `completed` defaults to `false`
- `title` length must be between 1 and 255 characters

**SQL Schema:**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
```

## API Endpoints

### 1. Get All Tasks
- **Method**: `GET`
- **Path**: `/tasks`
- **Description**: Retrieve all tasks from the database
- **Request Body**: None
- **Response Body**: Array of Task objects
- **Response Format**:
```json
[
  {
    "id": 1,
    "title": "Sample task",
    "completed": false
  },
  {
    "id": 2,
    "title": "Completed task",
    "completed": true
  }
]
```
- **Status Codes**:
  - `200 OK`: Successfully retrieved tasks
  - `500 Internal Server Error`: Database connection error

### 2. Create Task
- **Method**: `POST`
- **Path**: `/tasks`
- **Description**: Create a new task
- **Request Body**:
```json
{
  "title": "New task title"
}
```
- **Response Body**:
```json
{
  "id": 3,
  "title": "New task title",
  "completed": false
}
```
- **Status Codes**:
  - `201 Created`: Task created successfully
  - `400 Bad Request`: Invalid request body or missing title
  - `500 Internal Server Error`: Database error

### 3. Get Task by ID
- **Method**: `GET`
- **Path**: `/tasks/{id}`
- **Description**: Retrieve a specific task by its ID
- **Path Parameter**: `id` (integer)
- **Request Body**: None
- **Response Body**:
```json
{
  "id": 1,
  "title": "Sample task",
  "completed": false
}
```
- **Status Codes**:
  - `200 OK`: Task found and returned
  - `404 Not Found`: Task with given ID does not exist
  - `422 Unprocessable Entity`: Invalid ID format
  - `500 Internal Server Error`: Database error

### 4. Update Task
- **Method**: `PUT`
- **Path**: `/tasks/{id}`
- **Description**: Update an existing task's title
- **Path Parameter**: `id` (integer)
- **Request Body**:
```json
{
  "title": "Updated task title"
}
```
- **Response Body**:
```json
{
  "id": 1,
  "title": "Updated task title",
  "completed": false
}
```
- **Status Codes**:
  - `200 OK`: Task updated successfully
  - `404 Not Found`: Task with given ID does not exist
  - `400 Bad Request`: Invalid request body or missing title
  - `422 Unprocessable Entity`: Invalid ID format
  - `500 Internal Server Error`: Database error

### 5. Delete Task
- **Method**: `DELETE`
- **Path**: `/tasks/{id}`
- **Description**: Delete a task by its ID
- **Path Parameter**: `id` (integer)
- **Request Body**: None
- **Response Body**: None (empty)
- **Status Codes**:
  - `204 No Content`: Task deleted successfully
  - `404 Not Found`: Task with given ID does not exist
  - `422 Unprocessable Entity`: Invalid ID format
  - `500 Internal Server Error`: Database error

### 6. Toggle Task Completion
- **Method**: `PATCH`
- **Path**: `/tasks/{id}/complete`
- **Description**: Toggle the completion status of a task
- **Path Parameter**: `id` (integer)
- **Request Body**: None
- **Response Body**:
```json
{
  "id": 1,
  "title": "Sample task",
  "completed": true
}
```
- **Status Codes**:
  - `200 OK`: Task completion status toggled successfully
  - `404 Not Found`: Task with given ID does not exist
  - `422 Unprocessable Entity`: Invalid ID format
  - `500 Internal Server Error`: Database error

## Request/Response Validation

### Request Models
- **CreateTaskRequest**: `{ title: string }`
- **UpdateTaskRequest**: `{ title: string }`

### Response Models
- **TaskResponse**: `{ id: integer, title: string, completed: boolean }`
- **TaskListResponse**: Array of TaskResponse objects
- **ErrorResponse**: `{ detail: string }`

## Environment Configuration

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection string for Neon database
  - Format: `postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require`
  - Default: None (required)

### Optional Environment Variables
- `PORT`: Port number for the application server
  - Default: `8000`
- `LOG_LEVEL`: Logging level for the application
  - Default: `info`

### Example .env file
```
DATABASE_URL=postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
PORT=8000
LOG_LEVEL=info
```

## Middleware and Dependencies

### Required Dependencies
- `fastapi`: Web framework for building APIs
- `sqlmodel`: SQL toolkit and ORM combining SQLAlchemy and Pydantic
- `uvicorn`: ASGI server for running the application
- `psycopg2-binary`: PostgreSQL adapter for Python
- `pydantic`: Data validation library
- `python-dotenv`: Environment variable management

### Required Middleware
- **CORS Middleware**: Configured to allow requests from `http://localhost:3000`
  - Allow credentials: true
  - Allow methods: `GET, POST, PUT, DELETE, PATCH, OPTIONS`
  - Allow headers: `*`

### Additional Configuration
- **Database Connection Pooling**: Configured for optimal performance
- **Error Handling**: Custom HTTP exception handlers for consistent error responses
- **Logging**: Structured logging for debugging and monitoring
- **Startup Events**: Initialize database tables on application startup

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful GET, PUT, PATCH requests
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request format or validation error
- `404 Not Found`: Resource does not exist
- `422 Unprocessable Entity`: Invalid parameter format
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "detail": "Error message describing the issue"
}
```

## Security Considerations

### Input Validation
- All string inputs are validated for length and content
- Numeric inputs are validated for proper format
- SQL injection prevention through ORM usage

### Authentication
- No authentication required for initial implementation
- Future phases may include authentication middleware

### Rate Limiting
- Not implemented in initial version
- May be added in future phases if needed

## Performance Considerations

### Database Optimization
- Proper indexing on primary keys
- Connection pooling for database connections
- Efficient queries using SQLModel

### API Performance
- Pagination for large datasets (future enhancement)
- Caching strategies (future enhancement)
- Efficient serialization of data models

## Testing Requirements

### Unit Tests
- Database model validation
- CRUD operation testing
- API endpoint testing with mock database

### Integration Tests
- End-to-end API testing
- Database integration testing
- Error handling verification

## Deployment Considerations

### Production Readiness
- Proper logging configuration
- Health check endpoints
- Environment-based configuration
- Database migration strategy