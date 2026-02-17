
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
- [x] **Community**: Added standardized Issue/PR templates (HU/AC focused).
- [x] **Process**: Enforced Strict Development Philosophy and Traceability (HU -> Issue -> Commit) in `CONTRIBUTING.md`.
- [x] **Simulator Engine**: Defined `Animation` / `Frame` entities and `SimulatorService` domain logic.
- [x] **Simulator API**: POST /simulate endpoint implemented and tested.
- [x] **API Robustness**: Added strict pagination validation and global error handling [HU-005].
- [x] **Observability**: Implemented Structured Logging with `structlog` and Request ID tracing [HU-006][ADR-0007].

### Pending (Backlog for Phase 3)
- [x] **UI Design**: Wireframes and HTML/CSS structure for the main dashboard.
- [x] **Frontend Architecture**: Structured JS separated into Application (Engine), Domain (Simulation), and Infrastructure (Renderer).
- [x] **Frontend Implementation**: Dashboard rendering real sprite data structure (Tags, Versions).
- [x] **Simulator Integration**: "Simulate" button loads sprite image into Canvas engine.
- [ ] **Simulator Engine (Interactivity)**: Controls for playback, speed, and looping.
- [ ] **Player Component**: Reusable web component for playback.

### Blocked / Risks
- **Dependency**: Real OIDC credentials needed for production.

### Next Actionable Steps
1.  Implement Simulator Controls (Play/Pause, Speed).
2.  Implement "Upload Sprite" functionality to populate system.
3.  Add E2E test for full simulation flow (requires seeded data).
