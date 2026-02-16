# 4. Authentication Strategy (OIDC)

Date: 2026-02-15

## Status
Accepted

## Context
Spriter is a multi-user platform where users own their sprites. We need a secure, standard-compliant way to authenticate users. Instead of building a custom user management system (passwords, salts, emails), we will leverage OpenID Connect (OIDC).

## Decision
1.  **Provider Agnostic**: The implementation will support any OIDC provider (Keycloak, Auth0, Google) via environment configuration.
2.  **JWT Validation**: The backend will validate incoming Bearer tokens using RS256.
3.  **Clean Architecture**: 
    - A `UserContext` entity will be defined in the Domain to represent the current requester.
    - An `AuthenticationService` interface will be defined in Domain/Ports.
    - An `OIDCAuthenticationAdapter` will be implemented in Infrastructure.
4.  **Middleware**: A FastAPI dependency will extract and validate the user from the `Authorization` header.

## Consequences
- **Pros**: Offloads security responsibility to specialized providers, easy integration with enterprise SSO, standard-based.
- **Cons**: Requires a running OIDC provider for integration tests (or a mock).
