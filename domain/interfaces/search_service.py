from abc import ABC, abstractmethod
from typing import List
from domain.models.search import SearchResult

class ISearchService(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[SearchResult]:
        pass