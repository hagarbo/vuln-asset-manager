from abc import ABC, abstractmethod

class CVECollectorBase(ABC):
    @abstractmethod
    def fetch_cves(self, **kwargs):
        """Obtiene una lista de CVEs desde la fuente externa."""
        pass 