from typing import Dict, Iterator

from .common import Start, Stop


class Producer:
    def __init__(
            self,
            name: str = None,
    ):
        self.name = name or self.__class__.__name__

    @property
    def stream(
            self,
    ) -> Iterator[Dict]:
        yield Start()
        for item in self.to_stream():
            item.set_stage(stage=self.name)
            yield item
        # yield from self.to_stream()
        yield Stop()

    def to_stream(self) -> Iterator[Dict]:
        raise NotImplementedError
