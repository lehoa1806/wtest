from typing import Dict, Iterator, List

from .stage import Stage


class Filter(Stage):
    def __init__(
        self,
        output_columns: List[str] = None,
        name: str = None,
    ) -> None:
        super().__init__(name)
        self._output_columns = output_columns or []

    @property
    def output_columns(self) -> List[str]:
        return self._output_columns

    def process(self, item: Dict) -> Iterator:
        yield item
