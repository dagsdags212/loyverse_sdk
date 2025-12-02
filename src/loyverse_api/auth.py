from loyverse_api.core.config import config


class Auth:
    """Provides authentication to the Loyverse client"""

    def __init__(self, token: str | None = None):
        self.token = token or config.LOYVERSE_API_TOKEN
        if not self.token:
            raise ValueError("Loyverse API token must be provided.")

    @property
    def headers(self) -> dict[str, str]:
        """Setup HTTP headers"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
