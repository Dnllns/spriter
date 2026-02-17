# Project Rules

This document defines the strict rules and guidelines for the Spriter project. All contributors (human and AI) must adhere to these rules.

## Continuous Integration
1.  **Pipeline Priority**: Always verify and fix GitHub pipelines (`chk-ci`) before proceeding with new features. A failing pipeline is a critical blocker.
2.  **Linting**: Ensure code passes all linting (`ruff`) and type checking (`mypy`) rules before committing.
3.  **Testing**: All new features must be accompanied by relevant tests (Unit or E2E).

## Workflow
1.  **State Management**: Keep `docs/STATE.md` updated after every significant task.
2.  **Documentation**: Use `code` formatting or `[links]` when referencing files or specific concepts in documentation to pass consistency checks.

## Architecture
1.  **Clean Architecture**: Backend and Frontend must strictly follow Clean Architecture principles (Domain, Application, Infrastructure, Presentation/UI).
2.  **Dependency Injection**: Use `src/dependencies.py` for wiring system components.
