# Task 07: Create Task Item Component

## Description
Implement the individual task component with completion toggle, editing, and deletion functionality.

## Dependencies
- Task 01: Frontend Project Setup completed
- Task 02: TypeScript Type Definitions completed
- Task 03: API Integration Layer completed
- Directory structure with `components/` folder created

## Steps
1. Create `components/TaskItem.tsx`
2. Implement display of task title with completion status
3. Add checkbox for toggling completion
4. Implement inline editing functionality
5. Add delete button with confirmation
6. Add loading states for API operations
7. Style with Tailwind CSS

## Deliverable
- `components/TaskItem.tsx` with:
  - Task title display with strikethrough when completed
  - Checkbox to toggle completion status
  - Inline editing capability (double-click to edit)
  - Delete button with confirmation
  - Loading states during API operations
  - Error handling for API failures
  - Callback props for update, delete, and toggle operations
  - TypeScript typing for props

## Verification
- [ ] Task title displays with proper completion styling
- [ ] Checkbox toggles completion status
- [ ] Inline editing works (double-click to edit)
- [ ] Delete functionality works with confirmation
- [ ] Loading states are displayed during operations
- [ ] Error messages are shown for API failures
- [ ] Component is styled with Tailwind CSS
- [ ] All callback props function properly
- [ ] TypeScript props are properly typed