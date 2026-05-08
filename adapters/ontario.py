# Placeholder — will be implemented in the next phase
from .base import BaseSiteAdapter, Law


class OntarioAdapter(BaseSiteAdapter):
    """Adapter for ontario.ca/laws — Ontario Highway Traffic Act (JS SPA, needs Playwright)."""

    def fetch_laws(self) -> list[Law]:
        raise NotImplementedError("Ontario adapter not yet implemented")
