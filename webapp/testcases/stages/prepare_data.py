import logging
from typing import Dict, Iterator

from workflow.common import empty_data, Data, create_data_from_dict
from workflow.stage import Stage


class PrepareData(Stage):
    def __init__(
        self,
        name: str = None,
        data: Dict = None,
        log: str = None,
    ) -> None:
        super().__init__(name=name or 'PrepareData')
        self.data = data
        self.log = log

    def process(self, item: Dict) -> Iterator[Dict]:
        if self.log:
            logging.info(self.log)
        d = create_data_from_dict(self.data)
        yield d or empty_data()
