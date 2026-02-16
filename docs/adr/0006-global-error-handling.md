# ADR 0006: Global Error Handling and Domain Exceptions

## Status
Accepted

## Context
As the project grows, manual error handling in routers (e.g., checking for `None` and raising `HTTPException`) becomes repetitive and prone to inconsistency. We need a way to represent business-level errors (e.g., "Sprite not found", "Unauthorized action") in the Domain/Application layers and translate them to appropriate HTTP responses at the Presentation layer.

## Decision
We will implement a global error handling strategy using custom exceptions and FastAPI exception handlers:

1.  **Domain Exceptions**: Define custom exception classes in `src/domain/exceptions.py` (e.g., `SpriteNotFoundError`, `UnauthorizedError`). These classes should inherit from a base `DomainError`.
2.  **Service Responsibility**: Application services will raise these exceptions when business rules are violated (e.g., if a requested resource does not exist).
3.  **Global Handlers**: Register exception handlers in `src/main.py` using `app.exception_handler`. These handlers will catch domain exceptions and transform them into `JSONResponse` objects with the appropriate HTTP status codes (404 for not found, 403 for unauthorized, etc.).

## Consequences

### Positive
- **Clean Routers**: Presentation logic is simplified as it no longer needs to handle common error patterns manually.
- **Layer Decoupling**: Application and Domain layers remain independent of the web framework's exception system (HTTPException).
- **Consistency**: The API returns error messages in a consistent format across all endpoints.

### Negative
- **Traceability**: If not handled carefully, global handlers can hide the source of errors during debugging (mitigated by proper logging).
- **Boilerplate**: Requires defining an exception and a handler for each new type of business error.
