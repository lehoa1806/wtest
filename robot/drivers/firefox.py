from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from .browser import Browser


class Firefox(Browser):
    def get_options(self, headless: False) -> Options:
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        return options

    def get_browser(self, options) -> WebDriver:
        return WebDriver(options=options)
