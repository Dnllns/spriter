# Contributing to Spriter

Thank you for your interest in contributing! This project follows a "Project Memory Stack" philosophy where documentation and context are as important as code.

## Workflow

1.  **Read the Manifest**: Start by reading `AI_MANIFEST.md` to understand the vision and current phase.
2.  **Check State**: Look at `docs/STATE.md` to see what is currently being worked on and what is blocked.
3.  **Find a Task**: Pick an unassigned task from the `Pending` list in `docs/STATE.md`.
4.  **Create a Branch**: `git checkout -b feat/your-feature-name`.

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

- `feat(scope): add new feature`
- `fix(scope): resolve bug`
- `docs(scope): update documentation`
- `style(scope): format code`
- `refactor(scope): redesign code structure`
- `test(scope): add tests`
- `chore(scope): update build tasks`

## Pull Request Process

### Setup and Contribution

1.  **Install uv**: Follow instructions at [astral.sh/uv](https://astral.sh/uv).
2.  **Sync**: `uv sync --all-extras` (will setup `.venv` automatically).
3.  **Update Tests**: Ensure `uv run pytest` passes.
4.  **Lint**: Run `uv run ruff check .` and fix errors.
3.  **Update Docs**: If you changed architecture, add an ADR. If you completed a Phase item, update `AI_MANIFEST.md` and `docs/STATE.md`.
4.  **Description**: In your PR description, explain clearly *why* this change updates the project state.

## Project Memory Stack

The project relies on these files being up-to-date:
- `AI_MANIFEST.md`: Vision & Roadmap.
- `docs/STATE.md`: Current status dashboard.
- `docs/adr/`: Architectural Decision Records.
- `docs/DEVELOPMENT_RULES.md`: Technical constraints.

Please respect them.
