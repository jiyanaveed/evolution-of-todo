# Task 04: CRUD Operations Implementation

## Description
Implement all Create, Read, Update, and Delete operations for the Task entity following the specification.

## Dependencies
- Task 02: Database Models Implementation completed
- Task 03: Database Connection Implementation completed
- SQLModel and database session management configured

## Steps
1. Implement get_tasks function to retrieve all tasks from database
2. Implement get_task function to retrieve a specific task by ID
3. Implement create_task function to create a new task with validation
4. Implement update_task function to update an existing task's title
5. Implement delete_task function to delete a task by ID
6. Implement toggle_task_completion function to toggle completion status
7. Add proper error handling and validation for all operations
8. Ensure data integrity and proper session management

## Deliverable
- `backend/crud.py` containing:
  - get_tasks(session) - Returns list of all Task objects
  - get_task(session, task_id) - Returns specific Task or None
  - create_task(session, title) - Creates new Task with provided title
  - update_task(session, task_id, title) - Updates task title by ID
  - delete_task(session, task_id) - Deletes task by ID, returns boolean
  - toggle_task_completion(session, task_id) - Toggles completion status
  - Proper imports and type hints
  - Error handling for all operations

## Verification
- [ ] get_tasks function returns all tasks correctly
- [ ] get_task function returns specific task or None if not found
- [ ] create_task function creates new task with proper defaults
- [ ] update_task function updates only the title field
- [ ] delete_task function removes task and returns success status
- [ ] toggle_task_completion function toggles completion status
- [ ] All functions handle errors appropriately
- [ ] All functions properly manage database sessions
- [ ] Type hints are correctly implemented
- [ ] Functions follow the specification requirements