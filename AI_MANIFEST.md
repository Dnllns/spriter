# AI Manifest: Spriter - Advanced Sprite Repository & Simulator

## Vision
A high-performance codebase for managing animated sprites, offering versioning, preview, and simulation capabilities. The platform is designed with Clean Architecture, SOLID principles, and a "Full Python" backend philosophy, serving a modern, aesthetic frontend.

## Project Memory Stack (Mandatory)
This project enforces a cognitive persistence layer for both Human and AI contributors.

1.  **AI_MANIFEST.md**: The immutable vision, principles, and high-level roadmap.
2.  **docs/STATE.md**: The living dashboard of current progress, blockers, and next actions.
3.  **docs/adr/**: Architectural Decision Records explaining *why* technical choices were made.
4.  **docs/DEVELOPMENT_RULES.md**: strict rules for code quality and stack constraints.
5.  **docs/CONTRIBUTING.md**: Guidelines for workflow and commit standards.

Any significant change MUST update this stack to maintain context.

## Core Pillars
1.  **Clean Architecture**: Strict separation of concerns (Domain < Application < Infrastructure).
2.  **Quality First**: 100% Test Coverage (Unit, Integration, E2E), strict linting (Ruff), type safety.
3.  **Automation**: CI/CD for testing, docs, and versioning.
4.  **Observability**: Structured Logging and request tracing for efficient debugging.
5.  **Knowledge Driven**: This file and `docs/` serve as the source of truth for project state.
6.  **Strict Traceability**: Mandatory hierarchy Linking Commits -> Issues -> User Stories.

## Roadmap & Phases

### Phase 1: Foundation & Architecture
- [x] Initialize Git & Project Structure.
- [x] Define Domain Models (Sprite, Animation, Frame).
- [x] Setup Dev Environment (`uv` toolchain, Ruff, Pytest, Sphinx).
- [x] Implement Knowledge System (ADRs, Roadmap).

### Phase 2: Core Domain & API (Done)
- [x] Implement Sprite Upload/Versioning Logic.
- [x] Create REST API (FastAPI) for Sprite Management (Basic CRUD).
- [x] Implement Storage Service (Local/S3).
- [x] Add Authentication (OpenID Connect).
- [x] Setup PostgreSQL/SQLite and Alembic Migrations.

### Phase 3: Frontend & Simulator (Current)
- [ ] Design Modern UI (HTML/CSS/JS).
- [x] Implement Sprite Simulator API [HU-004].
- [ ] Implement Sprite Simulator Frontend (Canvas/JS).
- [ ] Build "Player" for animations.

### Phase 4: Community & Advanced Features
- [ ] Comments, Ratings, Tags.
- [x] Documentation Portal (Sphinx).
- [x] CI/CD Pipelines (GitHub Actions/GitLab CI).

### Current Context
Phase 3 (Frontend & Simulator) is active. Backend core, API robustness [HU-005], and Structured Logging [HU-006] are done. We are ready to start the **Frontend Dashboard**.

### Current State Verification
- [x] All knowledge tests pass.
- [x] Process HU/AC/PR/ADR documented in `CONTRIBUTING.md`.
- [x] Active Task: Design and implement the **Frontend Dashboard** (Phase 3 UI).
