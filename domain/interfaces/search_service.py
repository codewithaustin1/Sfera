from abc import ABC, abstractmethod
from domain.models.search import SearchResult

class ISearchService(ABC):
    @abstractmethod
    async def search(self, query: str) -> list[SearchResult]:
        pass