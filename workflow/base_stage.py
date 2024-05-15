from typing import Dict, Iterable, Iterator, List

from .common import Start, Stop


class BaseStage:
    def __init__(
        self,
        name: str = None,
    ) -> None:
        self.name = name or self.__class__.__name__

    @property
    def input_columns(self) -> List[str]:
        return []

    @property
    def output_columns(self) -> List[str]:
        return []

    def get_input_item(self, data: Dict):
        if isinstance(data, Start) or isinstance(data, Stop):
            return data
        if self.input_columns:
            out = {k: data[k] for k in self.input_columns}
            data['stage'] = data['stage']
            return out
        else:
            return data

    def get_output_item(self, data: Dict, **kwargs):
        if isinstance(data, Start) or isinstance(data, Stop):
            return data
        logged_data = kwargs.get('logged_data') or {}
        if self.output_columns:
            out_item = {k: data[k] for k in self.output_columns}
        else:
            out_item = data
        return {**out_item, **logged_data}

    def setup(self, item: Dict) -> Iterator:
        raise NotImplementedError

    def process(self, item: Dict) -> Iterator:
        raise NotImplementedError

    def teardown(self, item: Dict) -> Iterator:
        raise NotImplementedError

    def run(self, source: Iterable = None, **kwargs) -> Iterator:
        raise NotImplementedError
