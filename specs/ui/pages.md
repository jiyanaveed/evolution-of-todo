# UI Pages Specification

## Overview
The page structure for the Evolution of Todo application follows Next.js App Router conventions.

## Main Pages

### Home Page (app/page.tsx)
**Route**: `/`
**Purpose**: Main task management dashboard
**Features**:
- Authentication guard - redirects to login if not authenticated
- Task creation form at the top
- Task list display with all user tasks
- Integration with useTasks hook for CRUD operations
- Loading and error state management
- Responsive layout for all device sizes

### Login Page (app/login/page.tsx)
**Route**: `/login`
**Purpose**: User authentication interface
**Features**:
- Tabbed interface for login/registration
- Email and password input fields
- Form validation and error handling
- Authentication logic via AuthContext
- Redirect to home page after successful authentication
- Error messaging for failed attempts

## Layout Structure

### Root Layout (app/layout.tsx)
**Purpose**: Overall application structure
**Features**:
- HTML document structure
- Global styles and metadata
- Main content wrapper
- Header component integration

### Header Component (components/Header.tsx)
**Purpose**: Navigation and user information
**Features**:
- App title and branding
- User authentication status display
- Logout functionality when logged in
- Responsive design for mobile/desktop

## Authentication Flow

### Protected Routes
- Home page requires authentication
- Redirects to login if not authenticated
- Maintains authentication state across sessions

### Guest Routes
- Login page accessible to all users
- Redirects to home if already authenticated
- Supports both login and registration flows