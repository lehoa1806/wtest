from typing import Dict, Iterable, Set

from .common import Start, Stop


class Consumer:
    @property
    def required_columns(self) -> Set:
        return set()

    def setup(self, item: Dict) -> None:
        pass

    def process(self, item: Dict) -> None:
        raise NotImplementedError

    def teardown(self, item: Dict) -> None:
        pass

    def consume(self, source: Iterable[Dict]) -> None:
        for item in source:
            if isinstance(item, Start):
                self.setup(item)
            elif isinstance(item, Stop):
                self.teardown(item)
            else:
                if self.required_columns and not self.required_columns.issubset(set(item.keys())):
                    raise ValueError(f'Invalid data {item}. Required columns: {self.required_columns}.')
                self.process(item)
