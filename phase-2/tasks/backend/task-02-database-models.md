# Task 02: Database Models Implementation

## Description
Create the SQLModel database models for the Task entity and Pydantic request/response models according to the specification.

## Dependencies
- Task 01: Backend Project Setup completed
- SQLModel dependency installed

## Steps
1. Create Task SQLModel with id, title, and completed fields
2. Set up proper primary key configuration for id field
3. Configure title field as required string with proper constraints
4. Set completed field with boolean type and default value of false
5. Create Pydantic models for request validation (CreateTaskRequest, UpdateTaskRequest)
6. Create Pydantic model for response validation (TaskResponse)
7. Add proper type hints and validation

## Deliverable
- `backend/models.py` containing:
  - Task SQLModel with fields: id (int, primary key), title (str), completed (bool, default False)
  - CreateTaskRequest Pydantic model with title field
  - UpdateTaskRequest Pydantic model with title field
  - TaskResponse Pydantic model with id, title, and completed fields
  - Proper imports for SQLModel, Field, and other necessary components

## Verification
- [ ] Task model has correct fields with proper types
- [ ] id field is configured as primary key
- [ ] title field is required string field
- [ ] completed field defaults to False
- [ ] Request models have correct fields and validation
- [ ] Response model includes all required fields
- [ ] All models properly inherit from SQLModel/Pydantic
- [ ] Proper imports are included
- [ ] Models can be imported and used without errors