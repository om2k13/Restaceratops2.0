
import httpx, os, asyncio, logging, tenacity

log = logging.getLogger("agent.client")

class APIClient:
    """Async HTTP client wrapper supporting retries and bearer token."""
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: float = 30):
        self.base_url = base_url or os.getenv("BASE_URL", "http://localhost:8000")
        self.token = token or os.getenv("BEARER_TOKEN")
        self.timeout = timeout

    def _headers(self):
        hdrs = {"User-Agent": "Restaceratops/0.1"}
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
        return hdrs

    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=0.5, min=1, max=10),
        stop=tenacity.stop_after_attempt(3),
        reraise=True
    )
    async def request(self, method: str, path: str, **kwargs):
        # If path is a full URL, use it directly; otherwise combine with base_url
        if path.startswith(('http://', 'https://')):
            url = path
        else:
            url = self.base_url.rstrip("/") + path
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            resp = await client.request(method.upper(), url, headers=self._headers(), **kwargs)
            log.debug("HTTP %s %s -> %s", method, url, resp.status_code)
            return resp
