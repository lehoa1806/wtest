from __future__ import annotations

import logging
from enum import Enum

import pytest
from pyvirtualdisplay import Display

from configs.setting import Setting
from robot.robot import Robot


class LoginState(Enum):
    ANONYMOUS = 0
    ADMIN_LOGGED_IN = 1
    USER_LOGGED_IN = 2


class Machine:
    def __init__(self):
        self.display: Display | None = None
        self.robot:  Robot | None = None
        self.login_state = LoginState.ANONYMOUS
        self.start()

    def restart(self) -> None:
        logging.info('# ... Restarting machine')
        self.stop()
        self.start()

    def start(self) -> None:
        logging.info('# Start machine')
        self.display = (
            self.display
            or Display(visible=Setting().virtual_display_visible, size=Setting().virtual_display_size)
        )
        if not self.display.is_alive():
            self.display.start()
        self.robot = self.robot or Robot()
        self.robot.browser.maximize_window()

    def stop(self) -> None:
        logging.info('# Stop machine')
        if hasattr(self, 'robot') and self.robot:
            self.robot.close()
            self.robot = None
        if hasattr(self, 'display') and self.display:
            self.display.stop()

    def take_screenshot(self) -> None:
        if hasattr(self, 'robot'):
            self.robot.take_screenshot()


@pytest.fixture(scope="session")
def machine(request):
    logging.info('# Machine setUp')
    machine = Machine()
    yield machine
    logging.info('# Machine tearDown')
    machine.stop()
