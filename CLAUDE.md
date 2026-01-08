# The Evolution of Todo - CLAUDE Instructions

## Repository Overview
This is a Spec-Kit monorepo for "The Evolution of Todo" project, following the progression from CLI to distributed cloud-native AI systems.

## Project Structure
- `.spec-kit/` - Spec-Kit configuration and tools
- `specs/` - Current project specifications organized by category
- `specs-history/` - Historical specification snapshots by phase
- `frontend/` - Next.js web application
- `backend/` - FastAPI backend service
- Various root-level configuration files

## Development Workflow
1. **Spec-First Development**: All changes should be reflected in specs first
2. **Phase Evolution**: Follow the evolution from console → web → AI interfaces
3. **Spec Compliance**: Ensure implementations match specification requirements

## Spec Management
- Update specifications in `specs/` before making code changes
- Maintain historical snapshots in `specs-history/`
- Use `.spec-kit/config.yaml` for configuration

## Safety Constraints
- Do not break existing Phase I or Phase II functionality
- Preserve all existing working code in `frontend/` and `backend/`
- Only add, restructure, or document - do not delete or modify core logic

## Navigation
- `specs/` - Current specifications
- `specs-history/` - Phase snapshots
- `frontend/` - Web application code
- `backend/` - API and business logic