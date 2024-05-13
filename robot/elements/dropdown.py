from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from robot.common import do_and_sleep
from robot.locators import CSSLocator


class DropDown:
    def __init__(self, element: WebElement) -> None:
        self.html = Select(element)

    @do_and_sleep(level=1)
    def select_by_visible_text(
        self,
        text: str,
    ) -> None:
        """
        Select an option that display text matching the input text
        :param text: The visible text to select
        :return: None
        """
        self.html.select_by_visible_text(text)

    @classmethod
    def load_dropdown_by_css_selector(
        cls,
        parent: WebDriver | WebElement,
        css_selector: str,
    ) -> 'DropDown':
        """
        Locate a dropdown element by css selector.
          dropdown = DropDown.load_dropdown_by_css_selector('#foo')
        :param parent: a webdriver or the parent web element
        :param css_selector: CSS selector string, ex: 'a.nav#home'
        :return: WebElement - the dropdown if it was found
        """
        return cls(parent.find_element(*CSSLocator(css_selector)))
