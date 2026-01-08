# Task 06: Create Task Form Component

## Description
Implement the task creation form with validation and error handling.

## Dependencies
- Task 01: Frontend Project Setup completed
- Task 02: TypeScript Type Definitions completed
- Task 03: API Integration Layer completed
- Directory structure with `components/` folder created

## Steps
1. Create `components/TaskForm.tsx`
2. Implement form with input field for task title
3. Add form submission handling
4. Implement validation and error handling
5. Add loading state during API calls
6. Style with Tailwind CSS

## Deliverable
- `components/TaskForm.tsx` with:
  - Input field for task title
  - Submit button
  - Validation for empty titles
  - Loading state during creation
  - Error display for API failures
  - Callback prop for successful task creation
  - TypeScript typing for props

## Verification
- [ ] Form renders with input field and submit button
- [ ] Validation prevents empty task titles
- [ ] Loading state is displayed during API calls
- [ ] Error messages are displayed for API failures
- [ ] Successful task creation triggers callback
- [ ] Form resets after successful submission
- [ ] Component is styled with Tailwind CSS
- [ ] TypeScript props are properly typed