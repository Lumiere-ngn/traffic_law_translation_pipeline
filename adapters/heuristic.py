# Placeholder — will be implemented in the next phase
from .base import BaseSiteAdapter, Law


class HeuristicAdapter(BaseSiteAdapter):
    """Fallback adapter for unknown sites. Uses heuristics to extract laws."""

    def fetch_laws(self) -> list[Law]:
        raise NotImplementedError("Heuristic adapter not yet implemented")
