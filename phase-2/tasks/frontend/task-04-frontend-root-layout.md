# Task 04: Create Root Layout and Global Styles

## Description
Implement the main layout for the application with metadata and global styling.

## Dependencies
- Task 01: Frontend Project Setup completed
- Directory structure with `app/` folder created

## Steps
1. Create `app/layout.tsx` with proper Next.js 14 App Router format
2. Add metadata for title and description
3. Create `app/globals.css` with Tailwind directives
4. Add any global styles needed for the application

## Deliverable
- `app/layout.tsx` with:
  - Proper metadata configuration
  - HTML structure with lang attribute
  - Body with base styling classes
  - Children prop properly rendered
- `app/globals.css` with:
  - Tailwind directives (@tailwind base, components, utilities)
  - Any additional global styles

## Verification
- [ ] Layout component exports metadata correctly
- [ ] HTML structure includes proper lang attribute
- [ ] Tailwind directives are properly included in globals.css
- [ ] Global styles are applied to the application
- [ ] Children prop renders properly
- [ ] Application loads without layout errors