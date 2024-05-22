import logging
from contextlib import contextmanager
from time import sleep

from selenium.webdriver.common.by import By

from configs.setting import Setting
from robot.elements.button import Button
from webapp.testcases.base import BaseTestCase, testcase_options, web_element_wait_clickable


class Payment(BaseTestCase):
    @BaseTestCase.require_login_with_user('new_user')
    @BaseTestCase.machine
    def test_user_add_payment(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.add_payment()

    @BaseTestCase.require_login_with_user('new_user')
    @testcase_options(NumberOfPayment=5)
    @BaseTestCase.machine
    def test_user_add_many_payment(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.add_payment()

    @BaseTestCase.require_login_with_user('new_user')
    @BaseTestCase.machine
    def test_user_remove_primary_payment(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.remove_payment(is_priority=True)

    @BaseTestCase.require_login_with_user('new_user')
    @BaseTestCase.machine
    def test_user_remove_non_primary_payment(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.remove_payment()

    @BaseTestCase.require_login_with_user('new_user')
    @BaseTestCase.machine
    def test_user_make_primary_payment(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.make_default()

    def add_payment(self):
        loop = 1
        if hasattr(self, 'NumberOfPayment'):
            loop = self.NumberOfPayment
        current_number_payments = len(self.robot.find_elements_by_xpath(
            xpath='//button[@type="button" and @aria-haspopup="menu"]'
        ))
        if current_number_payments >= 5:
            sleep(1)
            self.robot.find_element_by_xpath(
                xpath='//button[@type="button" and text()="Add payment method" and @disabled]'
            )
            logging.info("Maximum number of payment methods reached")
            return

        for i in range(loop):
            if current_number_payments >= 5:
                self.robot.find_element_by_xpath(
                    xpath='//button[@type="button" and text()="Add payment method" and @disabled]'
                )
                logging.info("Maximum number of payment methods reached")
                return
            btn_add_payment = self.robot.find_element_by_xpath(
                xpath='//button[@type="button" and text()="Add payment method"]'
            )
            btn_add_payment.click()

            input_frame = self.robot.find_element_by_xpath(
                xpath='//iframe[@title="Secure card payment input frame"]'
            )

            with switch_to_frame(self.robot.browser, input_frame.get_attribute("name")):
                input_card_num = self.robot.find_element_by_xpath(
                    xpath='//input[@placeholder="Card number"]'
                )
                input_card_num.clear()
                input_card_num.send_keys("5555555555554444")
                # input_card_num.send_keys("4242424242424242")

                expire_date = self.robot.find_element_by_xpath(
                    xpath='//input[@placeholder="MM / YY"]'
                )

                cvc = self.robot.find_element_by_xpath(
                    xpath='//input[@placeholder="CVC"]'
                )

                expire_date.clear()
                expire_date.send_keys("12 / 27")

                cvc.clear()
                cvc.send_keys("123")

            btn_continue = Button.load_button_by_xpath_selector(
                parent=self.robot.browser,
                xpath_selector='//button[@type="button" and text()="Continue"]'
            )

            btn_continue.click()

            confirmation_form = self.robot.find_element_by_xpath(
                xpath='//form[@id="addPaymentMethodAddressForm"]'
            )

            btn_confirm = Button.load_button_by_xpath_selector(
                parent=confirmation_form,
                xpath_selector='//button[@type="submit" and text()="Add payment method"]'
            )

            btn_confirm.click_and_wait()

            current_number_payments += 1

    def remove_payment(self, is_priority: bool = False):
        btn_remove_xpath = '//button[@type="button" and @aria-haspopup="menu"]'
        all_btn_remove_payment = self.robot.find_elements_by_xpath(
            xpath=btn_remove_xpath
        )
        primary = f'{btn_remove_xpath}/preceding-sibling::*[1]/div/div/p[text()="Primary"]'
        btn_primary_xpath = f'{primary}/../../../../button'
        primary_provider_xpath = f'{primary}/../preceding-sibling::p[1]'

        btn_primary = self.robot.find_element_by_xpath(
            xpath=btn_primary_xpath
        )

        clicked_btn_provider = ""

        if is_priority:
            self.robot.scroll_to_element(btn_primary)
            btn_primary.click()
        else:
            for i in range(len(all_btn_remove_payment)):
                if all_btn_remove_payment[i].id != btn_primary.id:
                    provider = all_btn_remove_payment[i].find_element(
                        By.XPATH,
                        'preceding-sibling::div[1]/div/p'
                    )
                    clicked_btn_provider = provider.text
                    self.robot.scroll_to_element(all_btn_remove_payment[i])
                    all_btn_remove_payment[i].click()
                    break

        btn_remove = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector='//div[@role="menuitem" and text()="Remove"]'
        )

        btn_remove.click()

        if is_priority:
            btn_xpath = '//button[@type="button" and text()="OK"]'
            btn_confirm = Button.load_button_by_xpath_selector(
                parent=self.robot.browser,
                xpath_selector=btn_xpath
            )

            warning_text = self.robot.find_element_by_xpath(
                xpath=f'{btn_xpath}/../preceding-sibling::p[1]'
            )

            assert "In order to remove your default payment method, \
you first need to set a different payment method as your default!" == warning_text.text
        else:
            btn_xpath = '//button[@type="button" and text()="Delete"]'
            btn_confirm = Button.load_button_by_xpath_selector(
                parent=self.robot.browser,
                xpath_selector=btn_xpath
            )

            warning_text = self.robot.find_element_by_xpath(
                xpath=f'{btn_xpath}/../preceding-sibling::p[1]'
            )

            assert "Are you sure you want to remove this payment method? \
Removing it means you won't be able to pay your subscription without adding it again." == warning_text.text

        btn_confirm.click()

    def make_default(self):
        btn_remove_xpath = '//button[@type="button" and @aria-haspopup="menu"]'
        all_btn_remove_payment = self.robot.find_elements_by_xpath(
            xpath=btn_remove_xpath
        )
        primary = f'{btn_remove_xpath}/preceding-sibling::*[1]/div/div/p[text()="Primary"]'
        btn_primary_xpath = f'{primary}/../../../../button'
        primary_provider_xpath = f'{primary}/../preceding-sibling::p[1]'

        btn_primary = self.robot.find_element_by_xpath(
            xpath=btn_primary_xpath
        )

        clicked_btn_provider = ""
        for i in range(len(all_btn_remove_payment)):
            if all_btn_remove_payment[i].id != btn_primary.id:
                provider = all_btn_remove_payment[i].find_element(
                    By.XPATH,
                    'preceding-sibling::div[1]/div/p'
                )
                clicked_btn_provider = provider.text
                self.robot.scroll_to_element(all_btn_remove_payment[i])
                all_btn_remove_payment[i].click()
                break

        btn_make_primary = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector='//div[@role="menuitem" and text()="Make primary"]'
        )

        btn_make_primary.click_and_wait()

        new_primary = self.robot.find_element_by_xpath(
            xpath=primary_provider_xpath
        )

        assert new_primary.text == clicked_btn_provider, f'{new_primary.text} != {clicked_btn_provider}'


@contextmanager
def switch_to_frame(driver, frame_name):
    driver.switch_to.frame(frame_name)
    yield
    driver.switch_to.default_content()
