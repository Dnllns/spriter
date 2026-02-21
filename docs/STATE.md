
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
- [x] **Versioning**: Bumped to `0.6.0` with Animation Editor support.
- [x] **Releases**: Automated GitHub Releases with `uv build` artifacts (v0.2.6 deployed).
- [x] **Toolchain**: Migrated to `uv` for all workflows and local development.
- [x] **Security**: Enabled `CodeQL` scanning and `Dependabot` updates.
- [x] **Community**: Added standardized Issue/PR templates (HU/AC focused).
- [x] **Process**: Enforced Strict Development Philosophy and Traceability (HU -> Issue -> Commit) in `CONTRIBUTING.md`.
- [x] **Simulator Engine**: Defined `Animation` / `Frame` entities and `SimulatorService` domain logic.
- [x] **Simulator API**: POST /simulate endpoint implemented and tested.
- [x] **API Robustness**: Added strict pagination validation and global error handling [HU-005].
- [x] **Observability**: Implemented Structured Logging with `structlog` and Request ID tracing [HU-006][ADR-0007].
- [x] **Frame-based Storage**: Implemented backend slicing of sprite sheets into individual frame files (De-bundling) [HU-007].
- [x] **Embeddable Player**: Standing `<spriter-player>` Web Component with CORS/Base-URL support.
- [x] **Public/Private Flags**: Add `is_public` field to `Sprite` entity and database models.
- [x] **Mobile Optimization**: Refine `@media` queries in `index.css` for small screens.

### Pending (Backlog for Phase 3)
- [x] **UI Design**: Sidebar, Dashboard grid, and Glassy aesthetics.
- [x] **Frontend Architecture**: Structured JS (Engine, Simulation, Renderer).
- [x] **Frontend Implementation**: Dashboard rendering real sprite data (Tags, Versions).
- [x] **Simulator Integration**: "Simulate" button loads sprite frame-by-frame.
- [x] **Simulator Engine**: Controls for playback, speed, and looping.
- [x] **Refined Animation**: Multi-frame support via grid-detection.
- [x] **Flashy Landing Page**: Premium entry point with hero sections and glassmorphism.
- [x] **Player Component**: Standalone `<spriter-player>` Web Component for shared simulation embedding.

### Blocked / Risks
- **Dependency**: Real OIDC credentials needed for production.

- [x] **Analytics**: Implement a new `AnalyticsService` to track plays of embedded sprites [HU-009].
- [x] **Frame Browser**: Implement a UI section to browse and manage individual frames per sprite [HU-010].
- [x] **Privacy Logic**: Enforce `is_public` filtering in API endpoints [HU-008].
- [x] **Animation Editor**: Create and edit sequences in-browser (`HU-011`).
- [x] **Versioning**: Bumped to `0.6.0`.

### Next Actionable Steps
1. **Flashy Landing Page**: Design and implement a premium landing page with hero sections in `src/templates/landing.html`.
2. **Persistence Refinement**: Ensure database consistency when many versions exist.

### Quality Assurance
- [ ] Pipeline Green: Verify using `gh run list`.
- [ ] Adhere to `docs/RULES.md`: Check and fix any CI failures before new work.
