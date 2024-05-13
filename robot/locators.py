"""
Locator is a tuple of (by, path), which is used to locate a web element
"""
from selenium.webdriver.common.by import By


class IdLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.ID, locator))


class XpathLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.XPATH, locator))


class LinkTextLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.LINK_TEXT, locator))


class PartialLinkTextLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.PARTIAL_LINK_TEXT, locator))


class NameLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.NAME, locator))


class TagNameLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.TAG_NAME, locator))


class ClassNameLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.CLASS_NAME, locator))


class CSSLocator(tuple):
    def __new__(cls, locator: str):
        return tuple.__new__(cls, (By.CSS_SELECTOR, locator))
