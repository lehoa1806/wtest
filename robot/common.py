import functools
import logging
import random
import time
from contextlib import contextmanager
from enum import Enum

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from robot.locators import TagNameLocator


class BrowserType(Enum):
    CHROME = 'Chrome'
    FIREFOX = 'Firefox'


def do_and_sleep(func=None, *, level: int = 0):
    """
    A decorator to perform a sleep after executing a function
    :param func: The function to be decorated
    :param level: int
    """
    if func is None:
        return functools.partial(do_and_sleep, level=level)

    @functools.wraps(func)
    def wrapper_do_and_sleep(*args, **kwargs):
        value = func(*args, **kwargs)
        sort_delay = random.randint(1, 9)
        long_delay = random.randint(2, 4) * level
        delay = 0.1 * sort_delay + long_delay
        logging.info(f'Sleep for {str(round(delay, 2))} seconds')
        time.sleep(delay)
        return value
    return wrapper_do_and_sleep


def is_stale(element: WebElement) -> bool:
    """
    Check if the element is stale
    :param element: WebElement
    :return: bool
    """
    try:
        _ = element.size
        return False
    except StaleElementReferenceException:
        return True


@contextmanager
def wait_for_change(element: WebElement):
    """
    A context to wait for the element to be changed
    :param element: WebDriver
    """
    yield
    wait_time = 60
    while not is_stale(element) and wait_time > 0:
        time.sleep(1)
        wait_time -= 1


@contextmanager
def wait_for_page_load(browser: WebDriver):
    """
    A context to wait for the new page after switching from a html page
    :param browser: WebDriver
    """
    old_html = browser.find_element(*TagNameLocator('html'))
    yield
    wait_time = 60
    while not is_stale(old_html) and wait_time > 0:
        time.sleep(1)
        wait_time -= 1
