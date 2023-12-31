from abc import abstractmethod
from typing import List, Optional, Any

from pydantic import BaseSettings
from web_search.payload import TextPayload
from web_search.base_store import BaseStore


class BaseSourceConfig(BaseSettings):
    TYPE: str = "Base"

    class Config:
        arbitrary_types_allowed = True


class BaseSource(BaseSettings):
    store: Optional[BaseStore] = None

    @abstractmethod
    def lookup(self, config: BaseSourceConfig, **kwargs: Any) -> List[TextPayload]:
        pass

    class Config:
        arbitrary_types_allowed = True