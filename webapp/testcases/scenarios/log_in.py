from workflow.pipeline import Pipeline

from ..stages.log_in import LoginStage
from ..stages.prepare_data import PrepareData
from .base import Scenario


class LogInScenario(Scenario):
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.user = kwargs.get('user') or {}
        self.log = kwargs.get('log')

    @property
    def pipeline(self) -> Pipeline:
        return Pipeline(
            stage=PrepareData(data=self.user, log=self.log)
        ).add_stage(
            stage=LoginStage(robot=self.robot, skip_init_load=self.skip_init_load)
        )
