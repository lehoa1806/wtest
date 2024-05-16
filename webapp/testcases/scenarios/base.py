import logging

from robot.robot import Robot
from workflow.common import Data
from workflow.consumer import Consumer
from workflow.nope_consumer import NopeConsumer
from workflow.pipeline import Pipeline
from workflow.single_item_producer import SingleItemProducer
from workflow.task import Task


class Scenario(Task):
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.robot = kwargs.get('robot') or Robot()
        skip_init_load = kwargs.get('skip_init_load')
        self.skip_init_load = skip_init_load if skip_init_load is not None else True

    @property
    def consumer(self) -> Consumer:
        return NopeConsumer()

    @property
    def pipeline(self) -> Pipeline:
        raise NotImplementedError

    @property
    def producer(self):
        return SingleItemProducer(Data())

    def run(self) -> None:
        try:
            logging.info(f'{self.name} started ...')
            self.setup()
            self.consumer.consume(self.pipeline.run(self.producer.stream))
        except Exception as ex:
            logging.warning(f'{self.name} failed ...')
            raise ex
        finally:
            self.teardown()
            logging.info(f'{self.name} stopped ...')

    @classmethod
    def create_scenario(cls, **kwargs) -> 'Scenario':
        return cls(**kwargs)
