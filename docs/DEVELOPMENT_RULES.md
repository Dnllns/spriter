# Development Rules

These rules are non-negotiable for all contributions to Spriter.

## 1. Clean Architecture Strictness

- **Domain Layer**: Must be pure Python. NO framework dependencies (No FastAPI, No SQLAlchemy, No external libs). Only `pydantic` entities and `abc` interfaces are allowed.
- **Application Layer**: Contains business logic and use cases. Can depend on Domain. Can NOT depend on Infrastructure or Presentation details.
- **Infrastructure Layer**: Implements interfaces defined in Domain. Can use external libraries (SQLAlchemy, boto3, etc.).
- **Presentation Layer**: Entry points (FastAPI routers, CLI). Depends services in Application.

## 2. Code Quality & Testing

- **100% Test Coverage Target**: New features must include Unit and Integration tests.
- **Linting**: No code is merged with linting errors (`ruff check .`).
- **Formatting**: Code must be formatted with `ruff format .`.
- **Type Hints**: All function signatures must have type hints. Use Python 3.11+ syntax (`str | None`, `list[int]`).

## 3. Technology Stack specifics

- **Pydantic V2**: Use V2 models and syntax strictly.
- **SQLAlchemy 2.0+**: Use modern 2.0 syntax (selectors, async session).
- **FastAPI**: Use dependency injection for services.
- **Commit Messages**: Follow Conventional Commits format (`feat:`, `fix:`, `docs:`, `chore:`).

## 4. Project Memory

- **Update state**: If a task is completed, update `docs/STATE.md`.
- **Update Manifest**: If phase changes or major decision made, update `AI_MANIFEST.md`.
- **ADRs**: If a significant architectural decision is made, create a new ADR record.
