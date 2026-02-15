
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

### Pending (Backlog for Phase 2)
- [ ] **Authentication**: OpenID Connect integration (Keycloak/Auth0/Google). Currently mocked user (`mock_user`).
- [ ] **API refinement**: Error handling, pagination improvements, filter by tags/author.

### Blocked / Risks
- **Dependency**: Auth is required before multi-user features.

### Next Actionable Steps
1.  Configure OpenID Connect (OIDC) middleware for **Authentication** in `src/presentation/middleware.py`.
2.  Refine **API Error Handling** and **Pagination** in `src/presentation/routers.py`.
