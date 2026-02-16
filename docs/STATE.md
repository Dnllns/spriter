
# State of Spriter

This document tracks the current status of the project across different dimensions.

## Phase: 3 - Frontend & Simulator (In Progress)

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
- [x] **Documentation**: Automated Sphinx documentation build and deployment to GitHub Pages (Verified Live).
- [x] **Versioning**: Bumped to `0.2.6` with strict semantic versioning.
- [x] **Releases**: Automated GitHub Releases with `uv build` artifacts (v0.2.6 deployed).
- [x] **Toolchain**: Migrated to `uv` for all workflows and local development.
- [x] **Security**: Enabled `CodeQL` scanning and `Dependabot` updates.
- [x] **Community**: Added standardized Issue/PR templates.
- [x] **Simulator Engine**: Defined `Animation` / `Frame` entities and `SimulatorService` domain logic.

### Pending (Backlog for Phase 3)
- [ ] **UI Design**: Wireframes and HTML/CSS structure for the main dashboard.
- [ ] **Simulator Engine**: Core JavaScript/Canvas logic for sprite animation.
- [ ] **Simulator API**: Backend endpoints to serve run-time sprite data.
- [ ] **Player Component**: Reusable web component for playback.

### Blocked / Risks
- **Dependency**: Real OIDC credentials needed for production.

### Next Actionable Steps
1.  Implement **Simulator API** endpoints: `POST /simulate` to calculate frame for given time.
2.  Implement **API Error Handling** and **Pagination** in `src/presentation/routers.py`.

