import logging
import os
from configparser import ConfigParser, ExtendedInterpolation
from functools import cached_property
from typing import Dict

CONFIG_FILE = './config.ini'


class Config:
    """
    [robot]
    headless: true
    """
    @cached_property
    def _parser(self) -> ConfigParser | Dict:
        if not os.path.isfile(CONFIG_FILE):
            return {}
        try:
            _parser = ConfigParser(interpolation=ExtendedInterpolation())
            _parser.read(CONFIG_FILE)
            return _parser
        except Exception as e:
            logging.exception(e)
            return {}

    @cached_property
    def _global(self) -> Dict:
        try:
            return dict(self._parser['global'])
        except KeyError:
            return {}

    @cached_property
    def _robot(self) -> Dict:
        try:
            return dict(self._parser['robot'])
        except KeyError:
            return {}

    @cached_property
    def _virtual_display(self) -> Dict:
        try:
            return dict(self._parser['virtual_display'])
        except KeyError:
            return {}

    # Global configuration
    @property
    def app_domain(self) -> str | None:
        return self._global.get('app_domain')

    @property
    def log_level(self) -> str | None:
        return self._global.get('log_level')

    # Robot configuration
    @property
    def robot_debug(self) -> str | None:
        return self._robot.get('debug')

    @property
    def robot_browser_type(self) -> str | None:
        return self._robot.get('browser_type')

    @property
    def robot_headless(self) -> str | None:
        return self._robot.get('headless')

    @property
    def robot_timeout(self) -> str | None:
        return self._robot.get('timeout')

    # Virtual display configuration
    @property
    def vd_visible(self) -> str | None:
        return self._virtual_display.get('visible')

    @property
    def vd_width(self) -> str | None:
        return self._virtual_display.get('width')

    @property
    def vd_height(self) -> str | None:
        return self._virtual_display.get('height')
