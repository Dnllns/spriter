# Development Rules

These rules are non-negotiable for all contributions to Spriter.

## 1. Clean Architecture Strictness

- **Domain Layer**: Must be pure Python. NO framework dependencies (No FastAPI, No SQLAlchemy, No external libs). Only `pydantic` entities and `abc` interfaces are allowed.
- **Application Layer**: Contains business logic and use cases. Can depend on Domain. Can NOT depend on Infrastructure or Presentation details.
- **Infrastructure Layer**: Implements interfaces defined in Domain. Can use external libraries (SQLAlchemy, boto3, etc.).
- **Presentation Layer**: Entry points (FastAPI routers, CLI). Depends services in Application.

## 2. Toolchain: uv (Mandatory)

- **Dependency Management**: Use `uv` strictly. Do not use `pip` directly.
  - Add dependency: `uv add <package>`
  - Add dev dependency: `uv add --dev <package>`
  - Sync environment: `uv sync --all-extras`
- **Execution**: Run tools via `uv run` (e.g., `uv run pytest`).
- **Lockfile**: `uv.lock` must be committed and kept in sync.

## 3. Code Quality & Testing

- **100% Test Coverage Target**: New features must include Unit and Integration tests.
- **Linting**: No code is merged with linting errors (`uv run ruff check .`).
- **Formatting**: Code must be formatted with `uv run ruff format .`.
- **Type Hints**: All function signatures must have type hints. Use Python 3.11+ syntax.
## 3. Technology Stack specifics

- **Pydantic V2**: Use V2 models and syntax strictly.
- **SQLAlchemy 2.0+**: Use modern 2.0 syntax (selectors, async session).
- **FastAPI**: Use dependency injection for services.
- **Commit Messages**: Follow Conventional Commits format (`feat:`, `fix:`, `docs:`, `chore:`).

## 5. Repository Process (GitHub)

- **Mandatory HU/AC**: No code without a User Story (`docs/historias/HU-XXX.md`) and verified Acceptance Criteria.
- **Strict Branching**: `<type>/HU-XXX-description`. NO commits to `main`.
- **Merge Criteria**: PRs require 100% test pass, valid commits (with HU tags), and updated docs.
- **Detailed Workflow**: Reference `docs/CONTRIBUTING.md` for the full mandatory protocol.
