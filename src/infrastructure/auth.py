import httpx
from fastapi import HTTPException, status
from jose import JWTError, jwt

from ..config import settings
from ..domain.ports import AuthenticatorPort, User


class OIDCAuthenticatorAdapter(AuthenticatorPort):
    def __init__(self):
        self.issuer = settings.OIDC_ISSUER
        self.audience = settings.OIDC_AUDIENCE
        self.jwks = None

    async def _get_jwks(self):
        if self.jwks:
            return self.jwks

        # In a real OIDC provider, we fetch from discovery URL
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.issuer}/.well-known/jwks.json"
                response = await client.get(url)
                response.raise_for_status()
                self.jwks = response.json()
                return self.jwks
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not connect to OIDC provider: {str(e)}",
            ) from e

    async def authenticate(self, token: str) -> User:
        try:
            # Note: In production, fetch keys from JWKS first.
            # RS256 requires the public key.
            payload = jwt.decode(
                token,
                key="placeholder_key",  # Should be from JWKS
                audience=self.audience,
                issuer=self.issuer,
                algorithms=["RS256"],
            )
            return User(
                id=payload.get("sub"),
                email=payload.get("email"),
                username=payload.get("preferred_username") or payload.get("name"),
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
            ) from e


class MockAuthenticator(AuthenticatorPort):
    async def authenticate(self, token: str) -> User:
        """A simple mock that returns a user based on the 'token' content."""
        if token == "invalid-token":
            raise HTTPException(status_code=401, detail="Invalid token")

        return User(id=f"user_{token}", email=f"{token}@example.com", username=token)
