from typing import Dict, Iterable, Iterator

from .base_stage import BaseStage, Start, Stop


class Stage(BaseStage):
    def setup(self, item: Dict) -> Iterator:
        yield Start()

    def process(self, item: Dict) -> Iterator:
        raise NotImplementedError

    def teardown(self, item: Dict) -> Iterator:
        yield Stop()

    def run(self, source: Iterable = None, **kwargs) -> Iterator:
        source = source or []
        logged_columns = kwargs.get('logged_columns') or []
        for in_data in source:
            item = self.get_input_item(in_data)
            logged = {k: in_data.get(k) for k in logged_columns}
            if isinstance(item, Start):
                for out_data in self.setup(item):
                    yield self.get_output_item(out_data, logged_data=logged)
            elif isinstance(item, Stop):
                for out_data in self.teardown(item):
                    yield self.get_output_item(out_data, logged_data=logged)
            else:
                for out_data in self.process(item):
                    yield self.get_output_item(out_data, logged_data=logged)
