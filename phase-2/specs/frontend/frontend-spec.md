# Phase 2 Frontend Specification: Evolution of Todo

## 1. Overview

### Purpose
The frontend serves as the user interface for the Evolution of Todo application, providing an intuitive and responsive experience for managing tasks. It connects to a FastAPI backend to perform all CRUD operations on tasks.

### Target Users
- Individual users looking for a simple task management solution
- Users who want a clean, responsive interface for managing their to-do lists
- Developers looking to understand modern Next.js application patterns

### Expected Behavior and Goals
- Provide a responsive, mobile-first interface for task management
- Enable seamless CRUD operations for tasks
- Offer real-time updates without page refreshes
- Ensure fast load times and smooth interactions
- Maintain data consistency with the backend
- Provide clear feedback for user actions and errors

## 2. Pages and Routing

### Home Page (`/`)
- **Purpose**: Main task management interface
- **Content**:
  - Task creation form
  - Task list display
  - Empty state message when no tasks exist
- **Components**: TaskList, TaskForm, Header

### Task List Page (`/tasks`)
- **Purpose**: Dedicated view for task management (same as home page)
- **Content**:
  - Filter options (all, active, completed)
  - Sort options (by date created, title)
  - Task list with pagination if needed
- **Components**: TaskList, TaskFilters, Header

### Routing Strategy (Next.js App Router)
- `app/page.tsx` - Home page (main task interface)
- `app/tasks/page.tsx` - Task list page (optional, same as home)
- `app/tasks/[id]/page.tsx` - Task detail page (if implemented)
- `app/layout.tsx` - Root layout
- `app/globals.css` - Global styles

## 3. Components

### Core Components

#### TaskItem Component
- **Props**: task object, callbacks for update/delete/toggle
- **Features**:
  - Display task title with completion status
  - Toggle completion via checkbox
  - Inline editing capability
  - Delete button
  - Visual feedback for loading states

#### TaskList Component
- **Props**: array of tasks, callbacks for operations
- **Features**:
  - Render multiple TaskItem components
  - Handle empty state display
  - Show loading state while fetching
  - Display error messages

#### TaskForm Component
- **Props**: callback for task creation
- **Features**:
  - Input field for task title
  - Add task button
  - Validation feedback
  - Loading state during creation

#### Layout Components
- **Header**: App title and navigation
- **Footer**: Additional information or links
- **MainLayout**: Wraps main content with consistent structure

### UI Components
- **Buttons**: Primary, secondary, and danger variants
- **Input Fields**: Text inputs with validation states
- **Modals**: For confirmation dialogs
- **Loading Indicators**: For API operations
- **Notifications**: For success/error messages

## 4. State Management

### React State Management
- **Component-level state**: For individual component states (editing forms, loading states)
- **Context API**: For global state that needs to be shared across components (user preferences, theme)

### State Structure
```typescript
interface AppState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  updating: number | null; // ID of task being updated
}
```

### API Integration Points
- **useEffect hooks**: For initial data fetching
- **Event handlers**: For CRUD operations
- **Loading states**: To show visual feedback during API calls
- **Error handling**: To display API errors to the user

## 5. API Integration

### Backend Endpoints Required
- `GET /tasks` - Fetch all tasks
  - Response: `Task[]`
- `POST /tasks` - Create a new task
  - Request: `{ title: string }`
  - Response: `Task`
- `GET /tasks/{id}` - Fetch a specific task
  - Response: `Task`
- `PUT /tasks/{id}` - Update a task
  - Request: `{ title: string }`
  - Response: `Task`
- `DELETE /tasks/{id}` - Delete a task
  - Response: `204 No Content`
- `PATCH /tasks/{id}/complete` - Toggle task completion
  - Response: `Task`

### Data Fetching Strategy
- **Client-side fetching**: Using fetch or axios in useEffect hooks
- **SWR or React Query**: For advanced caching and revalidation (optional)
- **Error boundaries**: To handle API errors gracefully

### Expected Request/Response Payloads
```typescript
interface Task {
  id: number;
  title: string;
  completed: boolean;
}

interface CreateTaskRequest {
  title: string;
}

interface UpdateTaskRequest {
  title: string;
}
```

## 6. Styling & Theme

### CSS Framework
- **Tailwind CSS**: For utility-first styling approach
- **Custom CSS**: For specific styles not covered by Tailwind

### Color Scheme
- **Primary**: Blue (buttons, active states)
- **Secondary**: Gray (backgrounds, borders)
- **Success**: Green (success messages, completed tasks)
- **Danger**: Red (delete buttons, error messages)
- **Warning**: Yellow (warnings, pending actions)

### Typography
- **Font Family**: System font stack (San Francisco, BlinkMacSystemFont, Segoe UI, etc.)
- **Font Sizes**: Consistent scale (sm, base, lg, xl, 2xl)
- **Line Heights**: Appropriate for readability

### Spacing Guidelines
- **Consistent spacing**: Using Tailwind's spacing scale (0, 1, 2, 4, 8, etc.)
- **Responsive design**: Different spacing for mobile and desktop

## 7. User Interaction & UX

### Task Operations Behavior
- **Creating**:
  - Enter key in input field triggers creation
  - Clear input after successful creation
  - Show loading indicator during API call
- **Editing**:
  - Double-click task to enter inline edit mode
  - Enter key or save button to save changes
  - Escape key to cancel editing
- **Completing**:
  - Click checkbox to toggle completion
  - Visual feedback with strikethrough text
- **Deleting**:
  - Confirmation dialog for delete actions
  - Immediate UI removal after confirmation
  - Undo option (optional)

### Mobile Responsiveness
- **Touch-friendly**: Adequate touch targets (minimum 44px)
- **Responsive layout**: Flexbox/Grid for different screen sizes
- **Navigation**: Hamburger menu for smaller screens
- **Input fields**: Proper focus states and keyboard behavior

### Notifications & Messages
- **Success**: Green notification for successful operations
- **Error**: Red notification for failed operations
- **Loading**: Spinner or skeleton screens during API calls
- **Empty states**: Helpful messages when no data exists

## 8. Edge Cases

### Empty Task List
- Display friendly message encouraging task creation
- Provide clear call-to-action button
- Consider showing example tasks or tips

### API Errors
- Display user-friendly error messages
- Provide retry options
- Maintain offline capability if possible
- Show connection status indicators

### Invalid User Input
- Real-time validation feedback
- Clear error messages
- Prevent form submission with invalid data
- Proper input sanitization

### Network Issues
- Graceful degradation of functionality
- Offline-first approach if possible
- Clear communication of connection status
- Queue operations for retry when connection restored

## 9. Testing

### Unit Tests
- **Components**: Test rendering and interaction logic
- **Utils/Helpers**: Test utility functions
- **API Service**: Mock API calls and test error handling

### Integration Tests
- **Component interactions**: Test parent-child component communication
- **API integration**: Test actual API calls in a test environment
- **Form validation**: Test validation logic with various inputs

### End-to-End Tests (Optional)
- **Cypress or Playwright**: For critical user flows
- **Task creation flow**: From input to display
- **Task editing flow**: From edit to save
- **Task deletion flow**: With confirmation

### Testing Tools
- **Jest**: For unit testing
- **React Testing Library**: For component testing
- **Mock Service Worker (MSW)**: For API mocking

## 10. Deliverables

### Required Files Structure
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   └── types/
│       └── task.ts
├── components/
│   ├── TaskItem.tsx
│   ├── TaskList.tsx
│   ├── TaskForm.tsx
│   └── Header.tsx
├── lib/
│   ├── api.ts
│   └── task-api.ts
├── hooks/
│   └── useTasks.ts
├── package.json
├── tsconfig.json
└── README.md
```

### Component Specifications
- All components must be typed with TypeScript interfaces
- Components should be reusable and modular
- Follow React best practices (hooks, memoization, etc.)
- Proper error boundaries and loading states

### API Integration Requirements
- Centralized API service with axios or fetch
- Proper error handling and retry mechanisms
- Type-safe API calls using TypeScript
- Loading states for all API operations

### Documentation Requirements
- README with setup instructions
- Component documentation (JSDoc comments)
- API integration documentation
- Testing documentation

### Performance Requirements
- Fast initial load (under 3 seconds)
- Smooth interactions (60fps)
- Optimized bundle size (under 250KB)
- Proper image optimization

### Code Quality Requirements
- All code must follow TypeScript best practices
- ESLint and Prettier configuration
- Proper component folder structure
- Consistent naming conventions
- Comprehensive error handling
- Accessibility compliance (WCAG AA level)

---
*This specification follows spec-driven development principles and provides a complete roadmap for implementing the Phase 2 frontend of the Evolution of Todo application.*