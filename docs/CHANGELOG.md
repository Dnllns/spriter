# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **Simulator**: Implemented `POST /api/v1/simulate` endpoint to calculate current frame and progress [HU-004].
- **Simulator**: Added `Animation` and `Frame` domain entities and `SimulatorService` logic.
- **Process**: Enforced strict development philosophy (HU/AC/PR/ADR) in `CONTRIBUTING.md`.
- **API**: Implemented strict pagination validation (limit/offset) for `GET /api/v1/sprites` [HU-005].
- **API**: Added global exception mapping for `SpriteNotFoundError` and `UnauthorizedError` [HU-005][ADR-0006].
- **Security**: Enabled CodeQL workflow for automated security scanning.
- **Maintenance**: Enabled Dependabot for weekly dependency updates.
- **Documentation**: Added ADR 0005 (`uv` adoption) and ADR 0006 (Global Error Handling).

## [0.2.6] - 2026-02-16

### Fixed
- **CI**: Used `uv run python -m pytest` to enforce correct Python path resolution in tests.

## [0.2.5] - 2026-02-16

### Fixed
- **Release Workflow**: Added `permissions: contents: write` to allow automated release creation.
- **CI**: Added debug step to inspect Python path.

## [0.2.4] - 2026-02-16

### Changed
- **CI/CD**: Fully migrated all workflows (CI, Docs, Release) to use `uv` for dependency management and execution, improving speed and caching.
- **Dependencies**: Removed `docs/requirements.txt` in favor of `pyproject.toml` `docs` group.

## [0.2.3] - 2026-02-16

### Fixed
- **Dependencies**: Added `[project.optional-dependencies]` to `pyproject.toml` to fix `pip install .[test]` in CI.
- **CI**: Fixed `Test` job installing non-existent dependency group.

## [0.2.1] - 2026-02-16

### Fixed
- **CI/CD**: Fixed `PYTHONPATH` issues in CI, Knowledge Check, and Docs workflows.
- **Dependencies**: Upgraded deprecated GitHub Actions (v3 -> v4).

## [0.2.0] - 2026-02-16

### Added
- **CI/CD Pipelines**: Added GitHub Actions for continuous integration (testing, linting) and documentation deployment.
- **Documentation**: Enhanced Sphinx configuration with Furo theme and MyST parser. Added API documentation structure.
- **API**: Formalized API structure and documentation generation.
- **Project Structure**: Updated project configuration for version tracking.

### Feat
- Initialize project structure with Clean Architecture, Ruff, Pytest, and Sphinx.
