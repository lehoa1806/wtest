from typing import Dict, Iterator

from .common import Start, Stop


class Producer:
    @property
    def stream(
        self,
    ) -> Iterator[Dict]:
        yield Start()
        yield from self.to_stream()
        yield Stop()

    def to_stream(self) -> Iterator[Dict]:
        raise NotImplementedError
