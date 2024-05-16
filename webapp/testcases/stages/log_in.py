from typing import Dict, Iterator

from robot.robot import Robot
from workflow.common import empty_data

from ...pages.login_page import LoginPage
from .base import WebAppStage


class LoginStage(WebAppStage):
    def __init__(
        self,
        robot: Robot,
        skip_init_load: bool = True
    ) -> None:
        super().__init__(name='UserLogin', robot=robot, skip_init_load=skip_init_load)
        self.page = LoginPage(self.robot, skip_init_load=self.skip_init_load)

    def process(self, item: Dict) -> Iterator[Dict]:
        self.page.login(item['username'], item['password'])
        yield empty_data()
