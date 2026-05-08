# Adapter registry — maps domain to adapter class
from urllib.parse import urlparse


def get_adapter(url: str):
    """Return the appropriate site adapter for a given URL."""
    from .quebec import QuebecAdapter
    from .ontario import OntarioAdapter
    from .heuristic import HeuristicAdapter

    domain = urlparse(url).netloc.lower()

    ADAPTER_MAP = {
        "www.legisquebec.gouv.qc.ca": QuebecAdapter,
        "legisquebec.gouv.qc.ca": QuebecAdapter,
        "www.ontario.ca": OntarioAdapter,
        "ontario.ca": OntarioAdapter,
    }

    cls = ADAPTER_MAP.get(domain, HeuristicAdapter)
    return cls(url)
