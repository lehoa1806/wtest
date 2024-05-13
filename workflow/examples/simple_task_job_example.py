import argparse
import logging

from workflow.consumer import Consumer
from workflow.hybrid_consumer import HybridConsumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.serial_producer import SerialProducer
from workflow.stage import Stage
from workflow.task import Task


def get_stream(x: int = 10):
    for i in range(x):
        yield {
            'operand1': 2 * i,
            'operand2': 2 * i + 1,
            'operand3': 'unnecessary data',
        }


class SumStage(Stage):
    @property
    def input_columns(self):
        return ['operand1', 'operand2']

    def process(self, item):
        logging.info(
            f'SumStage: operand1 = {item["operand1"]}, operand2 = {item["operand2"]}')
        yield {'sum': item['operand1'] + item['operand2']}


class MultiplyStage(Stage):
    @property
    def input_columns(self):
        return ['operand1', 'operand2']

    def process(self, item):
        logging.info(
            f'MultiplyStage: operand1 = {item["operand1"]}, operand2 = {item["operand2"]}')
        yield {'multiply': item['operand1'] * item['operand2']}


class DictStage(Stage):
    def process(self, item):
        logging.info(
            f'DictStage: operand1 = {item["operand1"]}, operand2 = {item["operand2"]}, '
            f'sum = {item["sum"]}, multiply = {item["multiply"]}')
        output = {
            'operand1': item['operand1'],
            'operand2': item['operand2'],
            'sum': item['operand1'] + item['operand2'],
            'multiply': item['operand1'] * item['operand2'],
        }
        yield {'dict': output}


class ListStage(Stage):
    def process(self, item):
        logging.info(
            f'ListStage: operand1 = {item["operand1"]}, operand2 = {item["operand2"]}, '
            f'sum = {item["sum"]}, multiply = {item["multiply"]}')
        output = [
            item['operand1'],
            item['operand2'],
            item['operand1'] + item['operand2'],
            item['operand1'] * item['operand2'],
        ]
        yield {'list': output}


class SumConsumer(Consumer):
    def process(self, item):
        logging.info(
            f'SumConsumer subscribed for: Sum = {item["sum"]}')


class MultiplyConsumer(Consumer):
    def process(self, item):
        logging.info(
            f'MultiplyConsumer subscribed for: Multiply = {item["multiply"]}')


class DictListConsumer(Consumer):
    def process(self, item):
        logging.warning(
            f'DictListConsumer wants a list of the two operands, '
            f'sum and multiply results: = {item["list"]}')
        logging.warning(
            f'DictListConsumer also wants a dict of the two operands, '
            f'sum and multiply results: = {item["dict"]}')


class SimpleJob(Job):
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
           '--length',
           type=int,
           required=True,
           help='Length of the testing stream',
        )
        return parser.parse_args(namespace=argparse.Namespace())

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=SumStage(),
            logged_columns=['operand1', 'operand2'],
        ).add_stage(
            stage=MultiplyStage(),
            logged_columns=['operand1', 'operand2', 'sum'],
        )

    @property
    def consumer(self):
        list_consumer = HybridConsumer(
            consumers=[DictListConsumer()],
            pipeline=Pipeline(
                DictStage(),
                logged_columns=['operand1', 'operand2', 'sum', 'multiply'],
            )
        ).add_stage(
            stage=ListStage(),
            logged_columns=['dict'],
        )

        return HybridConsumer(
            consumers=[list_consumer]
        ).add_consumer(
            consumer=SumConsumer()
        ).add_consumer(
            consumer=MultiplyConsumer(),
        )

    @property
    def producer(self):
        return SerialProducer(get_stream(self.args.length))


class SimpleTask(Task):
    def __init__(self, **kwargs) -> None:
        self.length = kwargs.get('length', 10)
        super().__init__(**kwargs)

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=SumStage(),
            logged_columns=['operand1', 'operand2'],
        ).add_stage(
            stage=MultiplyStage(),
            logged_columns=['operand1', 'operand2', 'sum'],
        )

    @property
    def consumer(self):
        list_consumer = HybridConsumer(
            consumers=[DictListConsumer()],
            pipeline=Pipeline(
                DictStage(),
                logged_columns=['operand1', 'operand2', 'sum', 'multiply'],
            )
        ).add_stage(
            stage=ListStage(),
            logged_columns=['dict'],
        )

        return HybridConsumer(
            consumers=[list_consumer]
        ).add_consumer(
            consumer=SumConsumer()
        ).add_consumer(
            consumer=MultiplyConsumer(),
        )

    @property
    def producer(self):
        return SerialProducer(get_stream(self.length))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    # Call Task
    logging.info('=== Process SimpleTask ===')
    SimpleTask().process_task(length=5)
    # 1 5 9 13 17

    # Call Job
    logging.info('=== Process SimpleJOB ===')
    SimpleJob().main()
    # 1 5 9 13 17 21 25 29 33 37
