# ADR 0007: Adoption of Structured Logging with Structlog

## Status
Accepted

## Context
Standard Python logging produces flat text strings that are hard to parse and filter, especially when multiple requests are happening concurrently. To improve observability and debugging, we need structured data (JSON in production, pretty-printed in development) that includes contextual information like Request IDs.

## Decision
We will use `structlog` as the primary logging library:
1.  **Context Binding**: We will use `structlog`'s ability to bind context variables (like `request_id`) to the logger instance.
2.  **Formatters**:
    *   **Development**: Console renderer for readability.
    *   **Production**: JSON renderer for log aggregators.
3.  **Middleware**: A FastAPI middleware will be implemented to:
    *   Generate a unique `request_id` for every request.
    *   Initialize a request-local logger with that ID.
    *   Add the ID to the response headers.

## Consequences

### Positive
- **Searchability**: Logs can be easily queried by `request_id` or other fields.
- **Improved Debugging**: Every log line during a request will share the same ID, allowing us to follow the full flow.
- **Standardization**: All parts of the app will log in the same structured format.

### Negative
- **Complexity**: Slightly more complex setup than standard logging.
- **Dependency**: Adds `structlog` as a dependency.
