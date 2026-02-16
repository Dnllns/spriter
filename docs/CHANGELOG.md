# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.2.2] - 2026-02-16

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
