from __future__ import annotations

import logging
from functools import cached_property
from typing import Any, Tuple

from configs.config import Config
from configs.env import Env
from robot.common import BrowserType
from utils.singleton import Singleton


class Setting(metaclass=Singleton):
    def __init__(self):
        self.env = Env()
        self.config = Config()

    def get_attribute(self, name: str) -> Any:
        for config in [self.env, self.config]:
            attr = getattr(config, name, None)
            if attr is not None:
                return attr
        return None

    # Global configuration
    @cached_property
    def app_domain(self) -> str:
        app_domain = self.get_attribute('app_domain')
        if not app_domain:
            raise ValueError('app_domain is required')
        return app_domain

    @cached_property
    def s3_location(self) -> str:
        s3_location = self.get_attribute('s3_location')
        if not s3_location:
            raise ValueError('s3_location is required')
        return s3_location

    @property
    def log_level(self) -> int | None:
        name_to_level = {
            'CRITICAL': logging.CRITICAL,
            'FATAL': logging.FATAL,
            'ERROR': logging.ERROR,
            'WARN': logging.WARNING,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET,
        }
        level_name = (self.get_attribute('log_level') or 'error').upper()
        return name_to_level.get(level_name) or logging.ERROR

    # Robot configuration
    @cached_property
    def robot_debug(self) -> bool:
        return self.get_attribute('robot_debug') in {'true', 'True', 'TRUE'}

    @cached_property
    def robot_browser_type(self) -> BrowserType | None:
        browser_type = self.get_attribute('robot_browser_type')
        try:
            return (
                BrowserType(browser_type)
                if browser_type else None
            )
        except Exception as e:
            logging.exception(e)
            return None

    @cached_property
    def robot_headless(self) -> bool:
        return self.get_attribute('robot_headless') in {'true', 'True', 'TRUE'}

    @cached_property
    def robot_timeout(self) -> int | None:
        robot_timeout = self.get_attribute('robot_timeout')
        try:
            return (
                int(robot_timeout)
                if robot_timeout else None
            )
        except Exception as e:
            logging.exception(e)
            return None

    # Virtual display configuration
    @cached_property
    def virtual_display_visible(self) -> bool:
        return self.get_attribute('vd_visible') in {'true', 'True', 'TRUE'}

    @cached_property
    def virtual_display_size(self) -> Tuple[int, int]:
        try:
            vd_width = int(self.get_attribute('vd_width') or 1900)
            vd_height = int(self.get_attribute('vd_height') or 1200)
            return vd_width, vd_height
        except Exception as e:
            logging.exception(e)
            return 1900, 1200

    @cached_property
    def s3_endpoint_url(self) -> str:
        return self.get_attribute('s3_endpoint_url')

    @cached_property
    def s3_access_key(self) -> str:
        return self.get_attribute('s3_access_key')

    @cached_property
    def s3_secret_key(self) -> str:
        return self.get_attribute('s3_secret_key')
