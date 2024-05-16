import logging
from typing import Callable, Dict

import pytest
from selenium.common import NoSuchElementException, TimeoutException

from robot.elements.button import Button
from robot.locators import XpathLocator
from robot.robot import Robot
from webapp.conftest import LoginState, Machine
from webapp.data.test_data import TestData
from webapp.pages.admin_clients_page import AdminClientsPage
from webapp.pages.client_overview_page import ClientOverviewPage
from webapp.testcases.scenarios.log_in import LogInScenario


@pytest.mark.usefixtures("machine")
class BaseTestCase:
    """Base test class."""
    def __init__(self, machine, independent: bool = False):
        self.independent = independent
        self.machine: Machine = machine

    @property
    def robot(self) -> Robot:
        return self.machine.robot

    def set_up(self):
        pass

    def tear_down(self):
        pass

    @pytest.fixture(autouse=True, scope='class')
    def load_machine(self, machine):
        if self.independent and self.machine:
            self.machine.stop()
        elif not self.independent and not self.machine:
            self.machine = machine

    @staticmethod
    def machine(func: Callable = None) -> any:
        def call(self, *args, **kwargs):
            try:
                if self.machine and self.independent:
                    self.machine.restart()
                else:
                    self.machine = self.machine or Machine()
                self.set_up()
                return func(self, *args, **kwargs)
            except Exception as err:
                self.machine.robot.take_screenshot()
                raise err
            finally:
                self.tear_down()
        return call

    @staticmethod
    def require_admin_login(func: Callable = None) -> any:
        def call(self, *args, **kwargs):
            logging.info(self.machine)
            logging.info(self.machine.login_state)
            if self.machine.login_state == LoginState.USER_LOGGED_IN:
                self.logs_out()
            if self.machine.login_state == LoginState.ANONYMOUS:
                self.admin_logs_in()
            return func(self, *args, **kwargs)
        return call

    @staticmethod
    def require_user_login(func: Callable = None) -> any:
        def call(self, *args, **kwargs):
            if self.machine.login_state == LoginState.ADMIN_LOGGED_IN:
                self.logs_out()
            if self.machine.login_state == LoginState.ANONYMOUS:
                self.user_logs_in()
            return func(self, *args, **kwargs)
        return call

    def admin_logs_in(self):
        admin: Dict[str, str] = TestData().users.get('valid_admin')
        log = 'Loading a valid admin credentials ...'
        scenario = LogInScenario(
            robot=self.robot,
            user=admin,
            log=log,
            skip_init_load=False,
        )
        scenario.run()

        assert AdminClientsPage.URL in self.robot.current_url
        self.machine.login_state = LoginState.ADMIN_LOGGED_IN

    def user_logs_in(self):
        user: Dict[str, str] = TestData().users.get('valid_user')
        log = 'Loading a valid user credentials ...'
        scenario = LogInScenario(
            robot=self.robot,
            user=user,
            log=log,
            skip_init_load=False,
        )
        scenario.run()

        assert ClientOverviewPage.URL in self.robot.current_url
        self.machine.login_state = LoginState.USER_LOGGED_IN

    def logs_out(self, cancel: bool = False):
        store_switcher_css_selector = (
            # '#root > section > aside > div > div.storeSwitcher > div'
            '#root > div > div > div > div'
        )
        # logout_xpath_selector = '//li[@title="Log out"]'
        logout_xpath_selector = '//p[text()="Log out"]'
        # confirm_modal_xpath_selector = (
        #     '//div[@class="ant-modal-confirm-body-wrapper" and contains(., "Log out?")]'
        # )

        # confirm_logout_xpath_selector = (
        #     '//button[.//span[contains(text(), "Log out")]]'
        # )
        # cancel_logout_xpath_selector = (
        #     '//button[.//span[contains(text(), "Cancel")]]'
        # )

        confirm_logout_xpath_selector = (
            '//button[@type="button" and text()="Log out"]'
        )

        cancel_logout_xpath_selector = (
            '//button[@type="button" and text()="Cancel"]'
        )
        try:
            store_switcher = self.robot.wait_for_css_presence(
                css_selector=store_switcher_css_selector,
            )
        except (NoSuchElementException, TimeoutException):
            return

        store_switcher.click()
        self.robot.short_sleep()
        logout = self.robot.find_element_by_xpath(
            xpath=logout_xpath_selector,
        )
        logout.click()
        self.robot.short_sleep()

        # confirm_modal = self.robot.wait_for_presence(
        #     locator=XpathLocator(locator=confirm_modal_xpath_selector),
        # )

        # confirm_button = Button.load_button_by_xpath_selector(
        #     parent=confirm_modal,
        #     xpath_selector=confirm_logout_xpath_selector,
        # )
        # cancel_button = Button.load_button_by_xpath_selector(
        #     parent=confirm_modal,
        #     xpath_selector=cancel_logout_xpath_selector,
        # )
        confirm_button = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector=confirm_logout_xpath_selector,
        )
        cancel_button = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector=cancel_logout_xpath_selector,
        )
        if cancel:
            cancel_button.click_and_wait()
        else:
            confirm_button.click_and_wait()
            self.robot.long_sleep()
            self.machine.login_state = LoginState.ANONYMOUS
