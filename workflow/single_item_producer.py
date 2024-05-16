from typing import Any, Dict, Iterator

from .producer import Producer


class SingleItemProducer(Producer):
    def __init__(self, item: Dict[str, Any]) -> None:
        super().__init__(self.__class__.__name__)
        self.item = item

    def to_stream(self) -> Iterator[Dict]:
        yield self.item
