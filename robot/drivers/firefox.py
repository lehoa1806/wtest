import logging
import os
import subprocess

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

from configs import ROOT_DIR
from configs.setting import Setting
from .browser import Browser


class Firefox(Browser):
    def get_options(self, headless: False) -> Options:
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.enable_downloads = True
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", f"{ROOT_DIR}/logs")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

        return options

    def get_browser(self, options) -> WebDriver:
        service = None
        if Setting().log_level == logging.DEBUG:
            service = Service(log_output=os.path.join(ROOT_DIR, "logs/SELENIUM.STDOUT"))
        return WebDriver(options=options, service=service)
