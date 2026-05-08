# Placeholder — will be implemented in the next phase
from .base import BaseSiteAdapter, Law


class QuebecAdapter(BaseSiteAdapter):
    """Adapter for legisquebec.gouv.qc.ca — Quebec Highway Safety Code."""

    def fetch_laws(self) -> list[Law]:
        raise NotImplementedError("Quebec adapter not yet implemented")
