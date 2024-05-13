from typing import Dict, Iterable, Iterator, List

from .base_stage import BaseStage


class Pipeline(BaseStage):
    def __init__(
        self,
        stage,
        logged_columns: List[str] = None,
        name: str = None,
    ) -> None:
        name = name or f'Pipeline:{stage.name}'
        super().__init__(name)
        self.stages = [{
            'stage': stage,
            'logged_columns': logged_columns or [],
        }]

    def setup(self, item: Dict) -> Iterator:
        pass

    def process(self, item: Dict) -> Iterator:
        pass

    def teardown(self, item: Dict) -> Iterator:
        pass

    def run(self, source: Iterable = None, **kwargs) -> Iterator:
        source = source or []
        for stage_info in self.stages:
            stage = stage_info.get('stage')
            if not isinstance(stage, BaseStage):
                continue
            logged_columns = stage_info.get('logged_columns') or []
            source = stage.run(source, logged_columns=logged_columns)
        yield from source

    def add_stage(
        self,
        stage: BaseStage,
        logged_columns: List[str] = None,
        name: str = None,
    ) -> 'Pipeline':
        # TODO: Doesn't work if isinstace(stage, Pipeline). Correct this!!!
        name = name or stage.name
        self.name = f'{self.name}:{name}'
        self.stages.append({
            'stage': stage,
            'logged_columns': logged_columns or [],
        })
        return self
