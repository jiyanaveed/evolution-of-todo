# Final Locked Phase 3 Frontend Specification
Date: 2025-12-30
Status: LOCKED / APPROVED

## Authoritative Components
- ChatLayer (Orchestrator)
- VerbatimMessageList (History Display)
- ChatInput (Intent Capture)
- ReactiveTaskSidebar (Read-only View)
- TaskElement (Immutable for completed items)

## Action-Tool Sync
- Create -> create_todo_task
- Read -> get_todo_task
- List -> list_todo_tasks
- Update (Rename) -> update_todo_task (with confirmation)
- Update (Complete) -> update_todo_task (one-way)
- Delete -> delete_todo_task (with confirmation)

## Mandatory Rules
- Verbatim Persistence (No summaries)
- Two-Step Mutation (Delete/Rename)
- One-way Completion (False -> True)
- Stateless FETCH lifecycle
- Implicit Ownership via JWT

## Mandatory Warning
Any frontend functionality not listed here is strictly forbidden. Violations must be rejected.
