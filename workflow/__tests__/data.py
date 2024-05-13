import logging
from argparse import Namespace
from typing import Dict, Iterator, List

from ..consumer import Consumer
from ..job import Job
from ..pipeline import Pipeline
from ..producer import Producer
from ..single_item_producer import SingleItemProducer
from ..stage import Stage


class Stage1(Stage):
    @property
    def input_columns(self) -> List[str]:
        return ['key1', 'key2']

    def process(self, item: Dict) -> Iterator:
        yield {'key3': item['key1'] + item['key2']}


class Stage2(Stage):
    def process(self, item: Dict) -> Iterator:
        yield item


class Consumer1(Consumer):
    def process(self, item: Dict) -> None:
        logging.info(item)


class SimpleJob(Job):
    def parse_args(self) -> Namespace:
        pass

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=Stage1(),
            logged_columns=['key1', 'key2'],
        ).add_stage(
            stage=Stage2(),
        )

    @property
    def consumer(self) -> Consumer:
        return Consumer1()

    @property
    def producer(self) -> Producer:
        return SingleItemProducer(item={'key1': 1, 'key2': 2, })
