# Final Locked Phase 3 Specification
Date: 2025-12-30
Status: LOCKED / APPROVED

## Authoritative Tools
- create_todo_task
- get_todo_task
- list_todo_tasks
- update_todo_task
- delete_todo_task

## Safety Rules
- Two-Step Mutation Rule (Delete/Rename)
- Context-only user_id
- No Hallucination
- Verbatim History persistence
- FETCH -> APPEND -> RUN -> PERSIST -> RESPOND lifecycle

## Mandatory Warning
Any functionality not listed here must be rejected.
