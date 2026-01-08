# Agent Behavior Specification - Phase 3 - v1.2
Date: 2025-12-30
Status: Updated Draft

## Changes from v1.1
- Added LOCKED **Two-Step Mutation Rule**.
- Updated **Agent Decision Table** to reflect confirmation behavior for Delete and Update (rename).
- Updated **Agent Orchestration Pseudocode** to include a check for the Two-Step Mutation Rule.

## Key Components
- **LOCKED Decision Table**: Updated for 2-step confirmations.
- **LOCKED Two-Step Mutation Rule**: Mandatory confirmation for Delete and Irreversible Update.
- **LOCKED Lifecycle**: FETCH -> APPEND -> RUN -> PERSIST -> RESPOND.
