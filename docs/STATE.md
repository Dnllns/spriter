
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

### Pending (Backlog for Phase 2)
- [ ] **Storage Service**: Formalize implementation for file storage (S3/MinIO/Local abstraction). Currently barebones in `/tmp`.
- [ ] **Authentication**: OpenID Connect integration (Keycloak/Auth0/Google). Currently mocked user (`mock_user`).
- [ ] **API refinement**: Error handling, pagination improvements, filter by tags/author.

### Blocked / Risks
- **Risk**: File storage needs to be scalable. Using local `/tmp` is risky for anything beyond local dev. Need to prioritize robust storage strategy.
- **Dependency**: Auth is required before multi-user features.

### Next Actionable Steps
1.  Define Storage Interface in `domain` clearly and implement `LocalStorage` properly (with directory structure).
2.  Add authentication middleware.
