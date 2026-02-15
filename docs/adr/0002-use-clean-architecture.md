# 2. Use Clean Architecture

Date: 2026-02-15

## Status

Accepted

## Context

We need a flexible, maintainable, and testable architecture for the Spriter backend.

## Decision

We will use Clean Architecture with strict separation of concerns:
- **Domain**: Pure business logic (Entities, Interfaces). No external dependencies.
- **Application**: Use cases, interactors. Orchestrates domain logic.
- **Infrastructure**: Implementations of interfaces (DB, API clients, Filesystem).
- **Presentation**: Framework-specific code (FastAPI routers).

Dependencies only point inward (Presentation/Infrastructure -> Application -> Domain).

## Consequences

- Highly testable core logic.
- easy to swap infrastructure (e.g. SQLite -> PostgreSQL).
- Framework agnostic core.
- Slightly more boilerplate initially.
