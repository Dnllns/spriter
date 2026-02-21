# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2026-02-21

### Added
- **Public/Private Flags**: Added `is_public` field to `Sprite` entity and database models.
- **Mobile Optimization**: Refined `@media` queries in `styles.css` for small screens.

## [0.3.0] - 2026-02-18
- **Frontend Architecture**: Implemented Clean Architecture for the frontend (Application, Domain, Infrastructure, Service layers).
- **Simulator Integration**: Integrated `SimulatorEngine` (HTML5 Canvas) with `SimulatorService` and `DashboardUI`.
- **View Switching**: Implemented client-side navigation between "Dashboard" and "Simulator" views.
- **Sprite Rendering**: Dashboard now renders actual `Sprite` and `SpriteVersion` entities with tags and version counts.
- **Simulation Flow**: Added "Simulate" button to dashboard cards to load sprites into the simulator.
- **Infrastructure**: Added `CanvasRenderer` for dedicated rendering logic.
- **Testing**: Added E2E tests for frontend connectivity and unit tests for `SimulatorService` domain logic.
- **Dependencies**: Added `python-multipart` for handling file uploads.

### Changed
- **Refactor**: Split monolithic `engine.js` into modular components (`simulation.js`, `canvas_renderer.js`, `simulator_engine.js`).
- **Update**: `STATE.md` updated to reflect completion of key Phase 3 tasks.
- **Config**: Updated `.gitignore` to exclude additional Python artifacts.

## [0.2.6] - 2026-02-16

### Changed
- Improved CI configuration and addressed initial linting issues.
- Integrated `structlog` for structured logging.

### Fixed
- Addressed mypy type checking errors in core domain.
