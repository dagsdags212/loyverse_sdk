from loyverse_sdk.core.config import config
from loyverse_sdk.exceptions import ConfigurationError


class Auth:
    """Provides authentication to the Loyverse client"""

    def __init__(self, token: str | None = None):
        self.token = token or config.LOYVERSE_API_TOKEN
        if not self.token:
            raise ConfigurationError(
                "Loyverse API token must be provided. "
                "Set LOYVERSE_API_TOKEN environment variable or pass api_token parameter to LoyverseClient."
            )

    @property
    def headers(self) -> dict[str, str]:
        """Setup HTTP headers"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
