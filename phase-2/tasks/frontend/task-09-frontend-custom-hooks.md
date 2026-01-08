# Task 09: Create Custom Hooks for State Management

## Description
Implement custom React hooks for managing task state and API operations.

## Dependencies
- Task 01: Frontend Project Setup completed
- Task 02: TypeScript Type Definitions completed
- Task 03: API Integration Layer completed
- Directory structure with `hooks/` folder created

## Steps
1. Create `hooks/useTasks.ts`
2. Implement state for tasks array, loading, and error states
3. Add functions for fetching, creating, updating, deleting, and toggling tasks
4. Handle loading states for different operations
5. Implement error handling and state management

## Deliverable
- `hooks/useTasks.ts` with:
  - State for tasks array
  - State for loading indicators
  - State for error messages
  - Function to fetch all tasks
  - Function to create a task
  - Function to update a task
  - Function to delete a task
  - Function to toggle task completion
  - Loading states for different operations
  - Error handling for all operations
  - TypeScript typing for return values

## Verification
- [ ] Hook manages tasks state properly
- [ ] Loading states are correctly set during operations
- [ ] Error states are properly handled
- [ ] All task operations work correctly (CRUD)
- [ ] Completion toggle works properly
- [ ] Hook returns properly typed values
- [ ] Functions update state as expected
- [ ] API calls are properly integrated