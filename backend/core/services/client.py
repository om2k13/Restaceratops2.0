
import httpx, os, asyncio, logging
from typing import Optional

log = logging.getLogger("agent.client")

class APIClient:
    """Async HTTP client wrapper supporting retries and bearer token."""
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, timeout: float = 30):
        self.base_url = base_url or os.getenv("BASE_URL", "http://localhost:8000")
        self.token = token or os.getenv("BEARER_TOKEN")
        self.timeout = timeout

    def _headers(self):
        hdrs = {"User-Agent": "Restaceratops/0.1"}
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
        return hdrs

    async def request(self, method: str, path: str, **kwargs):
        """Make HTTP request with simple retry logic."""
        # If path is a full URL, use it directly; otherwise combine with base_url
        if path.startswith(('http://', 'https://')):
            url = path
        else:
            url = self.base_url.rstrip("/") + path
        
        # Simple retry logic (3 attempts)
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                    resp = await client.request(method.upper(), url, headers=self._headers(), **kwargs)
                    log.debug("HTTP %s %s -> %s", method, url, resp.status_code)
                    return resp
            except Exception as e:
                if attempt == 2:  # Last attempt
                    raise e
                log.warning(f"Request failed (attempt {attempt + 1}/3): {e}")
                await asyncio.sleep(0.5 * (2 ** attempt))  # Exponential backoff
