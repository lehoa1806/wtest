from robot.robot import Robot
from workflow.stage import Stage


class WebAppStage(Stage):
    def __init__(
        self,
        robot: Robot,
        name: str = None,
        skip_init_load: bool = True,
    ) -> None:
        super().__init__(name=name or 'WebAppStage')
        self.robot = robot
        self.skip_init_load = skip_init_load
