
# State of Spriter

This document tracks the current status of the project across different dimensions.

## Phase: 2 - Core Domain & API (In Progress)

### Completed (Done)
- [x] **Project Structure**: Clean Architecture folders in `src/`.
- [x] **Linting/Formatting**: Ruff configured and strictly enforced.
- [x] **Testing**: `pytest` setup with coverage (69% on last run).
- [x] **Domain Core**: `Sprite` and `SpriteVersion` entities defined.
- [x] **Database**: SQLAlchemy models + Alembic Initial Migration (`sprites` table).
- [x] **In-Memory PoC**: `InMemorySpriteRepository` for fast prototyping.
- [x] **Persistence Implementation**: `SqlAlchemySpriteRepository` fully implemented and tested.
- [x] **API Scaffolding**: FastAPI router for basic CRUD (Create, List, Get, Add Version).
- [x] **Storage Service**: Formalized `StoragePort` and `FileSystemStorageAdapter` (Async/Non-blocking).
- [x] **Authentication**: OIDC-ready architecture with `AuthenticatorPort` and `MockAuthenticator` (for dev).
- [x] **CI/CD**: GitHub Actions workflows for Testing, Linting, Security Scanning (Bandit), and Type Checking (MyPy).
- [x] **Documentation**: Automated Sphinx documentation build and deployment to GitHub Pages.
- [x] **Versioning**: Bumped to `0.2.5` with strict semantic versioning.
- [x] **Releases**: Automated GitHub Releases with `uv build` artifacts (v0.2.5 deployed).
- [x] **Toolchain**: Migrated to `uv` for all workflows and local development.

### Pending (Backlog for Phase 2)
- [ ] **OIDC Provider Setup**: Integration with a real provider (Keycloak/Auth0) in a staging environment.
- [ ] **API refinement**: Error handling, pagination improvements, filter by tags/author.

### Blocked / Risks
- **CI Testing**: `pytest` fails in CI (Exit Code 2) due to `src` path import issues, despite working locally. Needs layout refactor or path fix.
- **Dependency**: Real OIDC credentials needed for production.

### Next Actionable Steps
1.  Define **Simulator Domain Core** (Phase 3 transition): Animation frames, frame rates, and preview logic in `src/domain/simulator.py`.
2.  Implement **API Error Handling** and **Pagination** in `src/presentation/routers.py`.

