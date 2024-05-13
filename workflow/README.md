# workflow
A simple data processing workflow

```diagram
data                        stage --- consumer
  |                       /
producer --- stage --- stage --- stage --- consumer
                          \          \
                           \           stage --- consumer
                             consumer
```
# Introduction
### 1. Producers:
- Producer: parse data to data stream
- SingleItemProducer (input is a dictionary)
- SerialProducer (input is an iterator)
### 2. Stages:
- Stage: a middle step to process the data
- Pipeline: a sequence of stages
### 3. Consumers:
- Consumer: an endpoint to ingest output of pipeline
- HybridConsumer: a consumer with its own pipeline; or a group of consumers
### 4. Workers:
Put these above stuffs together to create a complete data processing workflow
- Job: receives config from terminal
- Task: config is set while initializing the object.
# Examples
### Test script
```bash
python3 -m workflow.examples.simple_task_job_example --length 5
```

### Usage example
```python
from workflow.consumer import Consumer
from workflow.job import Job
from workflow.pipeline import Pipeline
from workflow.serial_producer import SerialProducer
from workflow.stage import Stage


def get_stream():
    for i in range(10):
        yield {
            'operand1': 2 * i,
            'operand2': 2 * i + 1,
            'operand3': 'unnecessary data',
        }


class SimpleStage(Stage):
    @property
    def input_columns(self):
        return ['operand1', 'operand2']

    def process(self, item):
        yield {'sum': item['operand1'] + item['operand2']}


class SimpleConsumer(Consumer):
    def process(self, item):
        print(item.get('sum'))


class SimpleJob(Job):
    def parse_args(self):
        pass

    @property
    def pipeline(self):
        return Pipeline(
            stage=SimpleStage(),
        )

    @property
    def consumer(self):
        return SimpleConsumer()

    @property
    def producer(self):
        return SerialProducer(get_stream())


if __name__ == "__main__":
    # Step by step
    stream = SerialProducer(get_stream()).stream
    result = SimpleStage().run(stream)
    SimpleConsumer().consume(result)
    # 1 5 9 13 17 21 25 29 33 37

    # Call the worker
    SimpleJob().main()
    # 1 5 9 13 17 21 25 29 33 37
```
