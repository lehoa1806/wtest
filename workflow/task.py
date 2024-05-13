import logging

from .consumer import Consumer
from .pipeline import Pipeline
from .producer import Producer


class Task:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get('name') or self.__class__.__name__

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
            logging.info(f'{self.name} started ...')
            self.setup()
            self.consumer.consume(self.pipeline.run(self.producer.stream))
        except Exception as ex:
            logging.warning(f'{self.name} failed ...')
            logging.exception(str(ex))
        finally:
            self.teardown()
            logging.info(f'{self.name} stopped ...')

    @classmethod
    def process_task(cls, **kwargs) -> None:
        cls(**kwargs).main()
