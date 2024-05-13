
from selenium.webdriver.remote.webdriver import WebDriver

from configs.setting import Setting


class Browser:
    def __init__(self, options=None, **kwargs):
        headless = kwargs.get('headless', Setting().robot_headless)
        options = options or self.get_options(headless)
        self.browser = self.get_browser(options=options)

    def get_options(self, headless):
        raise NotImplementedError

    def get_browser(self, options) -> WebDriver:
        raise NotImplementedError
