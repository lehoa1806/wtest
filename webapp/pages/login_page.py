from configs.setting import Setting
from robot.elements.button import Button
from robot.locators import CSSLocator, NameLocator, XpathLocator

from .base import Page


class LoginPage(Page):
    URL = f'{Setting().app_domain}/login'

    EMAIL_FIELD = NameLocator('email')
    PASSWORD_FIELD = NameLocator('password')
    SUBMIT_BUTTON = XpathLocator('//button[@type="submit"]')
    EMAIL_ERROR_MESSAGE = CSSLocator('#LoginForm_email_help > div')
    ERROR_MESSAGE = CSSLocator("#LoginForm >div.d-flex > div")

    def login(self, email: str, password: str) -> None:
        """Login with email and password."""
        email_box = self.robot.find_element(self.EMAIL_FIELD)
        email_box.clear()
        email_box.send_keys(email)

        pwd_box = self.robot.find_element(self.PASSWORD_FIELD)
        pwd_box.clear()
        pwd_box.send_keys(password)

        submit_button = Button(self.robot.wait_until_clickable(self.SUBMIT_BUTTON))
        submit_button.click_and_wait()
        # self.robot.deep_sleep()
        self.robot.medium_sleep()

    def get_error_message(self):
        """Get error message."""
        return self.robot.find_element(self.ERROR_MESSAGE).text

    def get_email_error_message(self):
        """Get email error message."""
        return self.robot.find_element(self.EMAIL_ERROR_MESSAGE).text
