import logging
from datetime import datetime
from io import BytesIO
from typing import Callable, List, Tuple

import boto3
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from configs.setting import Setting
from robot.drivers.chrome import Chrome
from robot.drivers.firefox import Firefox

from .common import BrowserType, do_and_sleep, wait_for_page_load
from .elements.button import Button
from .elements.dropdown import DropDown
from .locators import (ClassNameLocator, CSSLocator, IdLocator,
                       LinkTextLocator, NameLocator, PartialLinkTextLocator,
                       TagNameLocator, XpathLocator)


class Robot:
    def __init__(
        self,
        browser: WebDriver = None,
        **kwargs,
    ) -> None:
        headless = kwargs.get('headless')
        self.headless = (
            Setting().robot_headless if headless is None else headless
        )
        self.debug = Setting().robot_debug
        self.timeout = kwargs.get('timeout') or Setting().robot_timeout
        self._browser = browser
        self._browser_type = kwargs.get('browser_type')
        self.s3_location = Setting().s3_location

    def __del__(self):
        if hasattr(self, '_browser') and self._browser:
            self._browser.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if hasattr(self, '_browser') and self._browser:
            self._browser.close()

    def close(self):
        if hasattr(self, '_browser') and self._browser:
            self._browser.close()

    @property
    def current_url(self) -> str:
        return self._browser.current_url

    @property
    def browser_type(self) -> BrowserType:
        return (
            self._browser_type
            or Setting().robot_browser_type
            or BrowserType.CHROME
        )

    @property
    def browser(self) -> WebDriver:
        self._browser = self._browser or self.get_browser(self.headless)
        return self._browser

    def get_browser(
        self,
        headless: bool = True,
    ) -> WebDriver:
        if self.browser_type == BrowserType.CHROME:
            return Chrome(headless=headless).browser
        else:
            return Firefox(headless=headless).browser

    @staticmethod
    def apply_debug(func: Callable = None) -> any:
        def call(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            if isinstance(res, WebElement) and self.debug:
                self.highlight_element(res)
            return res
        return call

    @do_and_sleep
    def short_sleep(self) -> None:
        pass

    @do_and_sleep(level=2)
    def long_sleep(self) -> None:
        pass

    @do_and_sleep(level=4)
    def deep_sleep(self) -> None:
        pass

    def take_screenshot(self) -> None:
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%Y-%m-%d-%H-%M-%S-%f')
        with BytesIO(self.browser.get_screenshot_as_png()) as screenshot:
            boto3.client('s3').upload_fileobj(
                screenshot,
                self.s3_location,
                f'screenshots/date={date}/{self.browser_type}-{time}.png'
            )
        logging.info(f'Screenshot was taken: {self.s3_location}/'
                     f'screenshots/date={date}/{self.browser_type}-{time}.png')

    @do_and_sleep(level=1)
    def load_url(self, url: str) -> None:
        logging.info(f'Start loading the page from URL: {url}')
        with wait_for_page_load(browser=self.browser):
            self.browser.get(url)
        logging.info(f'Page was loaded: {url}')

    @apply_debug
    def find_element(self, locator: Tuple) -> WebElement:
        """
        Find an element by its locator (a tuple of (By, Path)).
          id_locator = IdLocator('foo')
          element = self.find_element(id_locator)
        :param locator: locator of the element
        :return: WebElement
        """
        return self.browser.find_element(*locator)

    def find_elements(self, locator: Tuple) -> List[WebElement]:
        """
        Find elements by its locator (a tuple of (By, Path)).
          id_locator = IdLocator('foo')
          element = self.find_elements(id_locator)
        :param locator: locator of the element
        :return: list of WebElements
        """
        return self.browser.find_elements(*locator)

    def find_element_by_id(self, elem_id: str) -> WebElement:
        """
        Find an element by its id.
          element = self.find_element_by_id('foo')
        :param elem_id: The id of the element
        :return: WebElement
        """
        return self.find_element(IdLocator(elem_id))

    def find_elements_by_id(self, elem_id: str) -> List[WebElement]:
        """
        Find multiple elements by their id.
          elements = self.find_elements_by_id('foo')
        :param elem_id: The id of the elements
        :return: list of WebElements
        """
        return self.find_elements(IdLocator(elem_id))

    def find_element_by_xpath(self, xpath: str) -> WebElement:
        """
        Find an element by its xpath.
          element = self.find_element_by_xpath('//div/td[1]')
        :param xpath: The xpath locator of the element
        :return: WebElement
        """
        return self.find_element(XpathLocator(xpath))

    def find_elements_by_xpath(self, xpath: str) -> List[WebElement]:
        """
        Find multiple elements by their xpath.
          element = self.find_elements_by_xpath(
              "//div[contains(@class, 'foo')]"
          )
        :param xpath: The xpath locator of the element
        :return: list of WebElements
        """
        return self.find_elements(XpathLocator(xpath))

    def find_element_by_link_text(self, link_text: str) -> WebElement:
        """
        Find an element by link text.
          element = self.find_element_by_link_text('Sign In')
        :param link_text: The text of the element
        :return: WebElement
        """
        return self.find_element(LinkTextLocator(link_text))

    def find_elements_by_link_text(self, link_text: str) -> List[WebElement]:
        """
        Find elements by link text.
          elements = self.find_elements_by_link_text('Sign In')
        :param link_text: The text of the elements
        :return: list of WebElements
        """
        return self.find_elements(LinkTextLocator(link_text))

    def find_element_by_partial_link_text(self, link_text: str) -> WebElement:
        """
        Find an element by a partial match of its link text.
          element = self.find_element_by_partial_link_text('Sign')
        :param link_text: The text of the element to partially match on
        :return: WebElement
        """
        return self.find_element(PartialLinkTextLocator(link_text))

    def find_elements_by_partial_link_text(
        self,
        link_text: str,
    ) -> List[WebElement]:
        """
        Find elements by a partial match of their link text.
          elements = driver.find_elements_by_partial_link_text('Sign')
        :param link_text: The text of the elements to partial match on.
        :return: list of WebElements
        """
        return self.find_elements(PartialLinkTextLocator(link_text))

    def find_element_by_name(self, name: str) -> WebElement:
        """
        Find an element by name.
          element = driver.find_element_by_name('foo')
        :param name: The name of the element to find
        :return: WebElement
        """
        return self.find_element(NameLocator(name))

    def find_elements_by_name(self, name: str) -> List[WebElement]:
        """
        Find elements by name.
          elements = driver.find_elements_by_name('foo')
        :param name: The name of the elements to find.
        :return: list of WebElements
        """
        return self.find_elements(NameLocator(name))

    def find_element_by_tag_name(self, name: str) -> WebElement:
        """
        Find an element by tag name.
          element = driver.find_element_by_tag_name('h1')
        :param name: Name of html tag (eg: h1, a, span)
        :return: WebElement
        """
        return self.find_element(TagNameLocator(name))

    def find_elements_by_tag_name(self, name: str) -> List[WebElement]:
        """
        Find elements by tag name.
          elements = driver.find_elements_by_tag_name('h1')
        :param name: name of html tag (eg: h1, a, span)
        :return: list of WebElement
        """
        return self.find_elements(TagNameLocator(name))

    def find_element_by_class_name(self, name: str) -> WebElement:
        """
        Find an element by class name.
          element = driver.find_element_by_class_name('foo')
        :param name: The class name of the element to find.
        :return: WebElement
        """
        return self.find_element(ClassNameLocator(name))

    def find_elements_by_class_name(self, name: str) -> List[WebElement]:
        """
        Find elements by class name.
          elements = driver.find_elements_by_class_name('foo')
        :param name: The class name of the elements to find.
        :return: list of WebElement
        """
        return self.find_elements(ClassNameLocator(name))

    def find_element_by_css_selector(self, css_selector: str) -> WebElement:
        """
        Find an element by css selector.
          element = driver.find_element_by_css_selector('#foo')
        :param css_selector: CSS selector string, ex: 'a.nav#home'
        :return: WebElement - the element if it was found
        """
        return self.find_element(CSSLocator(css_selector))

    def find_elements_by_css_selector(
        self,
        css_selector: str,
    ) -> List[WebElement]:
        """
        Find elements by css selector.
          elements = driver.find_elements_by_css_selector('.foo')
        :param css_selector: CSS selector string, ex: 'a.nav#home'
        :return: list of WebElement
        """
        return self.find_elements(CSSLocator(css_selector))

    def wait_until_clickable(self, locator: Tuple):
        """
        Wait for an element to be clickable.
          id_locator = IdLocator('foo')
          element = self.wait_until_clickable(id_locator)
        :param locator: locator of the element
        :return: WebElement
        """
        return WebDriverWait(self.browser, self.timeout).until(
            ec.element_to_be_clickable(locator)
        )

    def wait_for_presence(self, locator: Tuple) -> WebElement:
        """
        Find an element and wait for it to be present using its locator (a
        tuple of (By, Path)).
          id_locator = IdLocator('foo')
          element = self.wait_for_presence(id_locator)
        :param locator: locator of the element
        :return: WebElement
        """
        return WebDriverWait(self.browser, self.timeout).until(
            ec.presence_of_element_located(locator))

    def wait_for_visibility(self, locator: Tuple) -> WebElement:
        """
        Find an element and wait for it to be visible using its locator (a
        tuple of (By, Path)).
          id_locator = IdLocator('foo')
          element = self.wait_for_visibility(id_locator)
        :param locator: locator of the element
        :return: WebElement
        """
        return WebDriverWait(self.browser, self.timeout).until(
            ec.visibility_of_element_located(locator))

    def wait_for_css_presence(self, css_selector: str) -> WebElement:
        """
        Find an element and wait for it to be present using its css_selector.
          element = self.wait_for_css_presence(css_selector)
        :param css_selector: CSS selector string, ex: 'a.nav#home'
        :return: WebElement
        """
        return self.wait_for_presence(CSSLocator(css_selector))

    def wait_for_tag_name_presence(self, name: str) -> WebElement:
        """
        Find an element and wait for it to be visible using its tag name.
          element = self.wait_for_tag_name_presence(name)
        :param name: The tag name of the element, ex: 'foo'
        :return: WebElement
        """
        return self.wait_for_presence(TagNameLocator(name))

    def wait_for_css_visibility(self, css_selector: str) -> WebElement:
        """
        Find an element and wait for it to be visible using its css_selector.
          element = self.wait_for_css_visibility(css_selector)
        :param css_selector: CSS selector string, ex: 'a.nav#home'
        :return: WebElement
        """
        return self.wait_for_visibility(CSSLocator(css_selector))

    def wait_for_class_visibility(self, name: str) -> WebElement:
        """
        Find an element and wait for it to be visible using its class name.
          element = self.wait_for_class_visibility(name)
        :param name: The class name of the element, ex: 'foo'
        :return: WebElement
        """
        return self.wait_for_visibility(ClassNameLocator(name))

    def wait_for_tag_name_visibility(self, name: str) -> WebElement:
        """
        Find an element and wait for it to be visible using its tag name.
          element = self.wait_for_tag_name_visibility(name)
        :param name: The tag name of the element, ex: 'foo'
        :return: WebElement
        """
        return self.wait_for_visibility(TagNameLocator(name))

    @do_and_sleep(level=2)
    def scroll(self) -> None:
        """
        Scroll down the page
        """
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )

    @do_and_sleep(level=1)
    def force_click(self, element: WebElement) -> None:
        """
        Click on an element that is present but having a permanent overlay
        :param element: Element will be clicked
        """
        self.browser.execute_script('arguments[0].click();', element)

    @do_and_sleep
    def set_style(self, element: WebElement, style: str) -> None:
        """
        Set style of an element
        :param element: The Element will be applied
        :param style: Style of the element
        """
        self.browser.execute_script('arguments[0].setAttribute("style", arguments[1]);', element, style)

    def highlight_element(self, element: WebElement):
        """Highlights (blinks) a Selenium Webdriver element."""
        original_style = element.get_attribute('style')
        self.set_style(element=element, style="background: yellow; border: 2px solid red;")
        self.set_style(element=element, style=original_style)

    @do_and_sleep
    def mouse_over(self, element: WebElement) -> None:
        """
        Perform a mouse over action on the giving element.
        :param element: WebElement
        """
        action = ActionChains(self.browser)
        action.move_by_offset(0, 0)
        action.move_to_element(element)
        action.perform()

    @do_and_sleep
    def switch_to_iframe(self, iframe: WebElement) -> None:
        """
        Move to the iframe.
        :param iframe: WebElement
        """
        self.browser.switch_to.frame(iframe)

    @do_and_sleep
    def switch_to_main_page(self) -> None:
        """
        Move back to the main page.
        """
        self.browser.switch_to.default_content()

    @do_and_sleep()
    def select_dropdown_by_css_selector(self, css_selector: str):
        """
        Locate a dropdown element by css selector.
          dropdown = self.select_dropdown_by_css_selector('#foo')
        :param css_selector: CSS selector string, ex: '#select'
        :return: WebElement - the dropdown if it was found
        """
        return DropDown.load_dropdown_by_css_selector(
            parent=self.browser, css_selector=css_selector)

    @do_and_sleep()
    def select_button_by_css_selector(self, css_selector):
        """
        Locate a button element by css selector.
          dropdown = self.select_button_by_css_selector('#foo')
        :param css_selector: CSS selector string, ex: '#select'
        :return: WebElement - the button if it was found
        """
        return Button.load_button_by_css_selector(
            parent=self.browser, css_selector=css_selector)

    @do_and_sleep()
    def select_child_button_by_css_selector(
        self,
        element: WebElement,
        css_selector: str,
    ):
        """
        Locate a button element by css selector.
          dropdown = self.select_button_by_css_selector('#foo')
        :param element: the parent web element
        :param css_selector: CSS selector string, ex: '#select'
        :return: WebElement - the button if it was found
        """
        return Button.load_button_by_css_selector(
            parent=element, css_selector=css_selector)
