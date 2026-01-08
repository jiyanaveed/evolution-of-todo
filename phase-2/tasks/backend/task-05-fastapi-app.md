# Task 05: FastAPI Application Implementation

## Description
Create the main FastAPI application with all specified endpoints, CORS configuration, and proper error handling.

## Dependencies
- Task 01: Backend Project Setup completed
- Task 02: Database Models Implementation completed
- Task 03: Database Connection Implementation completed
- Task 04: CRUD Operations Implementation completed
- All dependencies installed

## Steps
1. Initialize FastAPI application instance with proper title and version
2. Configure CORS middleware to allow requests from localhost:3000
3. Implement startup event to initialize database tables
4. Create GET /tasks endpoint to retrieve all tasks
5. Create POST /tasks endpoint to create new task with 201 status
6. Create GET /tasks/{id} endpoint to retrieve specific task
7. Create PUT /tasks/{id} endpoint to update task
8. Create DELETE /tasks/{id} endpoint to delete task with 204 status
9. Create PATCH /tasks/{id}/complete endpoint to toggle completion status
10. Add proper request/response models and status codes
11. Implement error handling with appropriate HTTP exceptions
12. Add proper type hints and documentation

## Deliverable
- `backend/main.py` containing:
  - FastAPI app instance with proper configuration
  - CORS middleware configured for localhost:3000
  - Startup event handler for database initialization
  - GET /tasks endpoint returning list of tasks with 200 status
  - POST /tasks endpoint creating task with 201 status
  - GET /tasks/{id} endpoint returning specific task or 404
  - PUT /tasks/{id} endpoint updating task or returning 404
  - DELETE /tasks/{id} endpoint deleting task with 204 status
  - PATCH /tasks/{id}/complete endpoint toggling completion with 200 status
  - All endpoints with proper request/response models
  - Error handling with HTTPException
  - Proper imports and type hints
  - Dependency injection for database sessions

## Verification
- [ ] FastAPI app is properly initialized
- [ ] CORS middleware allows requests from localhost:3000
- [ ] Startup event initializes database tables
- [ ] GET /tasks endpoint returns all tasks correctly
- [ ] POST /tasks endpoint creates task with 201 status
- [ ] GET /tasks/{id} endpoint returns specific task or 404
- [ ] PUT /tasks/{id} endpoint updates task or returns 404
- [ ] DELETE /tasks/{id} endpoint deletes task with 204 status
- [ ] PATCH /tasks/{id}/complete endpoint toggles completion
- [ ] All endpoints have proper status codes
- [ ] Request/response models are properly defined
- [ ] Error handling returns appropriate HTTP exceptions
- [ ] Type hints are correctly implemented
- [ ] Database sessions are properly injected
- [ ] All endpoints follow the specification requirements