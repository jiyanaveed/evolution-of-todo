# Task 02: Create TypeScript Type Definitions

## Description
Define TypeScript interfaces and types for the application according to the specification.

## Dependencies
- Task 01: Frontend Project Setup completed
- Directory structure with `types/` folder created

## Steps
1. Create `types/task.ts` file
2. Define Task interface with id, title, and completed properties
3. Define API request/response type interfaces
4. Add any additional shared type definitions

## Deliverable
- `types/task.ts` with the following interfaces:
  - `Task` interface: { id: number; title: string; completed: boolean }
  - `CreateTaskRequest` interface: { title: string }
  - `UpdateTaskRequest` interface: { title: string }
  - Any additional shared types as needed

## Verification
- [ ] Task interface has correct properties (id, title, completed)
- [ ] Request interfaces match API specification
- [ ] All types are properly exported
- [ ] TypeScript compiles without errors
- [ ] Types can be imported in other files successfully