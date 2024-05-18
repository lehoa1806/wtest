import logging
import os.path
import subprocess

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from configs import ROOT_DIR
from configs.setting import Setting
from .browser import Browser


class Chrome(Browser):
    def get_options(self, headless: False) -> Options:
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        options.enable_downloads = True
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("download.prompt_for_download", False)
        options.add_experimental_option("download.default_directory", f'{ROOT_DIR}/logs')

        return options

    def get_browser(self, options) -> WebDriver:
        service = None
        if Setting().log_level == logging.DEBUG:
            service = Service(log_output=os.path.join(ROOT_DIR, "SELENIUM.STDOUT"))
        return WebDriver(options=options, service=service)
