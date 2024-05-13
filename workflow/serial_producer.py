from typing import Dict, Iterator

from .producer import Producer


class SerialProducer(Producer):
    def __init__(self, source) -> None:
        self.source = source

    def to_stream(self) -> Iterator[Dict]:
        yield from self.source
