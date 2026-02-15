# 3. Storage Strategy

Date: 2026-02-15

## Status
Accepted

## Context
The project needs to store binary sprite files (images, potential json/xml) uploaded by users. We currently use a naive local file system implementation stored in `/tmp`, which is ephemeral and not scalable. We need a robust solution that works for local development but is production-ready for cloud deployment (S3/MinIO).

## Decision
1.  Define a formal `StoragePort` in the Domain layer (`src/domain/ports.py`) to decouple business logic from storage details.
2.  Implement a `FileSystemStorageAdapter` in the Infrastructure layer (`src/infrastructure/storage.py`) for local development and self-hosted scenarios.
3.  Use `aiofiles` for asynchronous file I/O to avoid blocking the main event loop in FastAPI.
4.  Structure the storage path logically: `{sprite_id}/v{version}/{filename}` to avoid collisions and keep organization.
5.  In the future, an `S3StorageAdapter` can be swapped in via dependency injection without changing a line of domain or application code.

## Consequences
- **Pros**: complete decoupling, non-blocking I/O, scalable path structure.
- **Cons**: slightly more complexity than just `open()`.
