from typing import Any, Dict

from workflow.consumer import Consumer


class NopeConsumer(Consumer):
    def process(self, row: Dict[Any, Any]) -> None:
        pass
