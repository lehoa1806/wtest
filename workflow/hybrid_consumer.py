from typing import Dict, Iterable, List

from .base_stage import BaseStage
from .consumer import Consumer
from .pipeline import Pipeline


class HybridConsumer(Consumer):
    def __init__(
        self,
        consumers: List[Consumer],
        pipeline: Pipeline = None,
    ) -> None:
        self.consumers = consumers
        self.pipeline = pipeline

    def setup(self, item: Dict) -> None:
        pass

    def process(self, item: Dict) -> None:
        raise NotImplementedError

    def teardown(self, item: Dict) -> None:
        pass

    def consume(self, source: Iterable[Dict]) -> None:
        source = self.pipeline.run(source) if self.pipeline else source
        for item in source:
            for consumer in self.consumers:
                consumer.consume([item])

    def add_stage(
        self,
        stage: BaseStage,
        logged_columns: List[str] = None,
        name: str = None,
    ) -> 'HybridConsumer':
        if self.pipeline:
            self.pipeline = self.pipeline.add_stage(
                stage=stage,
                logged_columns=logged_columns,
                name=name,
            )
        else:
            self.pipeline = Pipeline(
                stage=stage,
                logged_columns=logged_columns,
                name=name,
            )
        return self

    def add_consumer(self, consumer: Consumer) -> 'HybridConsumer':
        self.consumers.append(consumer)
        return self
