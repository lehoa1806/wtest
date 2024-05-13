import logging
from argparse import Namespace

from .consumer import Consumer
from .pipeline import Pipeline
from .producer import Producer


class Job:
    def __init__(self) -> None:
        self.args = self.parse_args()

    def parse_args(self) -> Namespace:
        raise NotImplementedError

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def consumer(self) -> Consumer:
        raise NotImplementedError

    @property
    def producer(self) -> Producer:
        raise NotImplementedError

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def main(self) -> None:
        try:
            logging.info('Start')
            self.setup()
            self.consumer.consume(self.pipeline.run(self.producer.stream))
        except Exception as ex:
            logging.warning('Failed')
            logging.exception(str(ex))
            raise SystemExit(1)
        finally:
            self.teardown()
            logging.info('Stop')
