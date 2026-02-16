# ADR 0004: Adoption of `uv` for Dependency Management and Workflow Automation

## Status
Accepted

## Context
The project previously relied on a mix of `pip` for dependency installation, `hatchling` for building (configured via `pyproject.toml`), and standard GitHub Actions using `actions/setup-python` with pip caching. While functional, this setup led to slower CI execution times, lack of deterministic lockfiles (unless manually managed), and fragmented command execution across local and CI environments.

Specifically, we encountered issues with:
1.  **CI Speed**: Installing dependencies via pip in every workflow run was suboptimal.
2.  **Path Resolution**: Using standard `pytest` in CI sometimes led to import errors (e.g., `ModuleNotFoundError: No module named 'src'`) due to environment differences.
3.  **Reproducibility**: Lack of a strict lockfile meant potential drift between dev and CI environments.

## Decision
We have decided to adopt **[uv](https://github.com/astral-sh/uv)** as the primary toolchain for the project.

Key changes include:
1.  **Dependency Management**: All dependencies are managed in `pyproject.toml` and locked in `uv.lock`.
2.  **Installation**: `uv sync` is used to install environments, replacing `pip install`.
3.  **Execution**: `uv run` is used to execute tools (e.g., `uv run pytest`, `uv run ruff`), ensuring commands run in the correct environment with proper path configuration.
4.  **CI/CD**: GitHub Actions now use `astral-sh/setup-uv` for setup and caching.
5.  **Builds**: `uv build` replaces `python -m build`.

## Consequences

### Positive
*   **Performance**: Dependency resolution and installation are significantly faster (often 10-100x), speeding up CI workflows.
*   **Determinism**: `uv.lock` ensures that exact versions are installed everywhere.
*   **Unified Workflow**: A single tool handles venv creation, package installation, tool execution, and building.
*   **Simplicity**: Contributors only need to install `uv` to get started.

### Negative
*   **Tooling Change**: Requirement for contributors to install and learn basic `uv` commands (mitigated by documentation updates).
*   **CI Complexity**: Initial setup required tuning commands (e.g., `uv run python -m pytest` vs `uv run pytest`) to handle path resolution correctly, though this is now resolved.

## Compliance
All documentation (`README.md`, `DEVELOPMENT_RULES.md`, `CONTRIBUTING.md`) has been updated to mandate `uv` usage. CI workflows are strictly using `uv`.
