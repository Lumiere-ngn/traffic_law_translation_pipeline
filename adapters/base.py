"""
Base classes and data models for all site adapters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Law:
    """Canonical representation of a single law/section extracted from any site."""
    id: str            # e.g. "QC_C-24.2_s310", "ON_HTA_s144(1)"
    title: str         # Short heading, if present
    body: str          # Full plain-text of the law
    source_url: str    # Canonical URL of the page
    section: str       # Chapter / Part / Division grouping
    raw_html: str = "" # Preserved for debugging / re-parsing


class BaseSiteAdapter(ABC):
    """Interface that every site-specific adapter must implement."""

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def fetch_laws(self) -> list[Law]:
        """Fetch and parse all laws from the site. Returns a list of Law objects."""
        ...
