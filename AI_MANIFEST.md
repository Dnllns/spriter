# AI Manifest: Spriter - Advanced Sprite Repository & Simulator

## Vision
A high-performance codebase for managing animated sprites, offering versioning, preview, and simulation capabilities. The platform is designed with Clean Architecture, SOLID principles, and a "Full Python" backend philosophy, serving a modern, aesthetic frontend.

## Core Pillars
1.  **Clean Architecture**: Strict separation of concerns (Domain < Application < Infrastructure).
2.  **Quality First**: 100% Test Coverage (Unit, Integration, E2E), strict linting (Ruff), type safety.
3.  **Automation**: CI/CD for testing, docs, and versioning.
4.  **Knowledge Driven**: This file and `docs/` serve as the source of truth for project state.

## Roadmap & Phases

### Phase 1: Foundation & Architecture (Current)
- [x] Initialize Git & Project Structure.
- [x] Define Domain Models (Sprite, Animation, Frame).
- [x] Setup Dev Environment (Ruff, Pytest, Sphinx).
- [x] Implement Knowledge System (ADRs, Roadmap).

### Phase 2: Core Domain & API
- [ ] Implement Sprite Upload/Versioning Logic.
- [x] Create REST API (FastAPI) for Sprite Management (Basic CRUD).
- [ ] Implement Storage Service (Local/S3).
- [ ] Add Authentication (OpenID Connect).
- [x] Setup PostgreSQL/SQLite and Alembic Migrations.

### Phase 3: Frontend & Simulator
- [ ] Design Modern UI (HTML/CSS/JS).
- [ ] Implement Sprite Simulator (Canvas/JS interacting with Python Backend).
- [ ] Build "Player" for animations.

### Phase 4: Community & Advanced Features
- [ ] Comments, Ratings, Tags.
- [ ] Documentation Portal (Sphinx).
- [ ] CI/CD Pipelines (GitHub Actions/GitLab CI).

## Current Context
Project initialized. Directory structure being created.
