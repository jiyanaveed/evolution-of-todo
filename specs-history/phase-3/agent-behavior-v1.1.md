# Agent Behavior Specification - Phase 3 - v1.1
Date: 2025-12-30
Status: Updated Draft

## Changes from v1.0
- Added LOCKED Agent Decision Table with required parameters and confirmation behavior.
- Added LOCKED Conversation Lifecycle Rules defining conversational identity and stateless execution sequence.
- Explicitly prohibited memory, summarization, and inferred state.

## Key Components
- **LOCKED Decision Table**: Exhaustive mapping for CRUD.
- **LOCKED Lifecycle**: FETCH -> APPEND -> RUN -> PERSIST -> RESPOND sequence.
- **Stateless Execution**: Mandatory DB-backed context.
- **Prohibitions**: No memory, no summarization, no inferred state.
