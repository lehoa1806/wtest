from typing import Dict

from webapp.conftest import LoginState
from webapp.data.test_data import TestData
from webapp.pages.admin_clients_page import AdminClientsPage
from webapp.pages.client_overview_page import ClientOverviewPage
from webapp.pages.login_page import LoginPage
from webapp.testcases.base import BaseTestCase
from webapp.testcases.scenarios.log_in import LogInScenario


class LogInLogOut(BaseTestCase):
    @BaseTestCase.machine
    def test_admin_logs_in_successfully(self):
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

    @BaseTestCase.machine
    def test_user_logs_in_successfully(self):
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

    @BaseTestCase.machine
    def test_user_logs_in_unsuccessfully(self):
        user: Dict[str, str] = TestData().users.get('invalid_user_invalid_email')
        log = 'Loading an invalid user with bad email ...'
        scenario = LogInScenario(
            robot=self.robot,
            user=user,
            log=log,
            skip_init_load=False,
        )
        scenario.run()

        assert LoginPage.URL in self.robot.current_url
        assert LoginPage(self.robot).get_email_error_message() == 'Please enter a valid email address.'

        user: Dict[str, str] = TestData().users.get('invalid_user_invalid_password')
        log = 'Loading an invalid user with incorrect password ...'
        scenario = LogInScenario(
            robot=self.robot,
            user=user,
            log=log,
            skip_init_load=True,
        )
        scenario.run()
        assert LoginPage.URL in self.robot.current_url
        assert LoginPage(self.robot).get_error_message() == 'Failed to process login :: Password is not correct'

        user: Dict[str, str] = TestData().users.get('invalid_user_unregistered_email')
        log = 'Loading an invalid user with unregistered email ...'
        scenario = LogInScenario(
            robot=self.robot,
            user=user,
            log=log,
            skip_init_load=True,
        )
        scenario.run()
        assert LoginPage.URL in self.robot.current_url
        assert LoginPage(self.robot).get_error_message() == (
            "Failed to process login :: User with email janedoe@gmail.com doesn't exist"
        )

    @BaseTestCase.machine
    @BaseTestCase.require_admin_login
    def test_admin_logs_out_successfully(self):
        self.logs_out()
        assert LoginPage.URL in self.robot.current_url

    @BaseTestCase.machine
    @BaseTestCase.require_user_login
    def test_user_logs_out_successfully(self):
        self.logs_out()
        assert LoginPage.URL in self.robot.current_url

    @BaseTestCase.machine
    @BaseTestCase.require_user_login
    def test_user_logs_out_cancel(self):
        self.logs_out(cancel=True)
        assert ClientOverviewPage.URL in self.robot.current_url
