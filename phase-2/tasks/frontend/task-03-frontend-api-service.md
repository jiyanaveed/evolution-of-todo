# Task 03: Set up API Integration Layer

## Description
Create the API service layer with axios configuration and implement all required backend endpoint calls.

## Dependencies
- Task 01: Frontend Project Setup completed
- Task 02: TypeScript Type Definitions completed
- Directory structure with `lib/` folder created

## Steps
1. Create `lib/api.ts` with axios configuration
2. Set up base URL with fallback to localhost
3. Add request and response interceptors
4. Create `lib/task-api.ts` with all required API functions
5. Implement all endpoint functions: getTasks, createTask, getTask, updateTask, deleteTask, toggleTaskCompletion

## Deliverable
- `lib/api.ts` with axios instance and configuration
- `lib/task-api.ts` with taskApi object containing:
  - getTasks(): Promise<Task[]>
  - getTask(id: number): Promise<Task>
  - createTask(taskData: CreateTaskRequest): Promise<Task>
  - updateTask(id: number, taskData: UpdateTaskRequest): Promise<Task>
  - deleteTask(id: number): Promise<void>
  - toggleTaskCompletion(id: number): Promise<Task>

## Verification
- [ ] Axios instance is properly configured with base URL
- [ ] All API functions return proper Promise types
- [ ] Functions use correct HTTP methods and endpoints
- [ ] Error handling is implemented in interceptors
- [ ] TypeScript types are properly applied to all functions
- [ ] Functions can be imported and used in other files