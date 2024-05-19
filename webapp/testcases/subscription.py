import logging
import unicodedata
import random
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from configs.setting import Setting
from selenium.webdriver.support import expected_conditions as ec

from robot.elements.button import Button
from webapp.pages.subscription import all_subscriptions
from webapp.testcases.base import BaseTestCase, testcase_options


class Subscription(BaseTestCase):

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user('new_user')
    @testcase_options(NewUser=True)
    def test_new_user_view_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.show_subscriptions()

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user()
    def test_old_user_view_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.show_subscriptions()

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user()
    def test_user_buy_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.buy_subscription()

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user()
    @testcase_options(ChangePayment=True)
    def test_user_buy_subscription_with_not_default_payment(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.buy_subscription()

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user("user_with_subscription")
    def test_user_cancel_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.unsubscribe()

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user("user_with_subscription")
    def test_user_cancel_and_keep_current_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.unsubscribe(is_keep_plan_active=True)

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user("user_with_subscription")
    def test_user_resubscribe_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.unsubscribe(is_keep_plan_active=True)
        btn_resubscribe = self.robot.find_element_by_xpath(
            xpath='//button[@type="button" and text()="Resubscribe"]'
        )
        btn_resubscribe.click()
        btn_confirm = Button.load_button_by_xpath_selector(
            parent=self.robot.driver.browser,
            xpath_selector='(//button[@type="button" and text()="Resubscribe"])[2]'
        )
        btn_confirm.click_and_wait()

        status = self.robot.find_element_by_xpath(
            xpath='//p[text()="Status"]/following-sibling::div[1]/p'
        )
        assert status.text == 'Active', f'{status.text} != Active'

    def show_subscriptions(self) -> List[WebElement]:
        is_new_user = hasattr(self, 'NewUser') and self.NewUser is True
        subscription_cards = self.retrieve_subscriptions(is_new_user)

        assert len(subscription_cards) == 10

        subs = []
        for c in subscription_cards:
            s = extract_subscription_info(c)
            subs.append(s)
        logging.info(subs)
        for s in subs:
            assert all_subscriptions[s["name"]]["price"] == s[
                "price"], f'{s["price"]} != {all_subscriptions[s["name"]]["price"]}'
            assert all_subscriptions[s["name"]]["size"] == s[
                "size"], f'{s["size"]} != {all_subscriptions[s["name"]]["size"]}'
            assert all_subscriptions[s["name"]]["rate"] == s[
                "rate"], f'{s["rate"]} != {all_subscriptions[s["name"]]["rate"]}'

        return subscription_cards

    def buy_subscription(self) -> None:
        is_new_user = hasattr(self, 'NewUser') and self.NewUser is True
        subscription_cards = self.retrieve_subscriptions(is_new_user)

        idx = random.randint(0, len(subscription_cards) - 1)
        sub_card = subscription_cards[idx]

        plan_name = unicodedata.normalize("NFKD", sub_card.find_element(By.CSS_SELECTOR,
                                                                        'div > div > div > div > p').get_attribute(
            "innerText"))

        btn_subscribe = web_element_wait_clickable(sub_card, (By.XPATH, './/button[text()="Subscribe"]'))
        btn_subscribe.click()

        btn_next = self.robot.find_elements_by_xpath(
            xpath='//button[@type="button" and text()="Next"]'
        )

        btn_next[0].click()
        btn_next[1].click()

        if hasattr(self, 'ChangePayment') and self.ChangePayment is True:
            btn_combobox = self.robot.find_element_by_xpath(
                xpath='//button[@role="combobox"]'
            )
            btn_combobox.click()

            second_opt = self.robot.find_element_by_xpath(
                xpath='(//div[@role="option"])[2]'
            )
            second_opt.click()

        btn_purchase = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector='//button[@type="button" and text()="Purchase"]'
        )

        btn_purchase.click_and_wait()

        current_plan = self.robot.find_element_by_xpath(
            xpath='//p[starts-with(text(), "Current plan")]'
        )
        assert current_plan.text == f'CURRENT PLAN: {plan_name}', f'{current_plan.text} != CURRENT PLAN: {plan_name}'

        status = self.robot.find_element_by_xpath(
            xpath='//p[text()="Status"]/following-sibling::div[1]/p'
        )
        assert status.text == 'Active', f'{status.text} != Active'

    def retrieve_subscriptions(self, is_new_user: bool = False):
        button_show_subscription_xpath = '//button[text()="Show subscription plans"]' if is_new_user \
            else '//button[text()="See all plans"]'

        subscript_card_xpath = (
            '//div[contains(@class, "bg-card") and contains(@class, "@container")]'
        )

        show_sub_btn = self.robot.find_element_by_xpath(
            xpath=button_show_subscription_xpath
        )
        show_sub_btn.click()

        subscription_cards = self.robot.find_elements_by_xpath(
            xpath=subscript_card_xpath
        )
        return subscription_cards

    def unsubscribe(self, is_keep_plan_active: bool = False):
        btn_unsubscribe = self.robot.find_element_by_xpath(
            xpath='//button[@type="button" and text()="Unsubscribe"]'
        )
        btn_unsubscribe.click()

        if not is_keep_plan_active:
            # Default is checked
            btn_keep_plan_active = self.robot.find_element_by_xpath(
                xpath='//button[@type="button" and @role="checkbox"]'
            )
            # Uncheck
            btn_keep_plan_active.click()

        btn_confirm = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector='//button[@type="button" and text()="Confirm"]'
        )
        btn_confirm.click_and_wait()

        status = self.robot.find_element_by_xpath(
            xpath='//p[text()="Status"]/following-sibling::div[1]/p'
        )
        if not is_keep_plan_active:
            assert status.text == 'Expired', f'{status.text} != Expired'
        else:
            self.robot.find_element_by_xpath(
                xpath='//button[@type="button" and text()="Resubscribe"]'
            )
            assert status.text == 'Unsubscribing', f'{status.text} != Unsubscribing'


class SubscriptionInfo(dict):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self[k] = v


def extract_subscription_info(card) -> SubscriptionInfo:
    name_css = (
        'div > div > div > div > p'
    )
    size_css = (
        'div > div > div > h4'
    )
    price_css = (
        'div > div > div > div:nth-child(3)'
    )
    rate_css = (
        'div > div > div:nth-child(2)'
    )

    name = unicodedata.normalize("NFKD", card.find_element(By.CSS_SELECTOR, name_css).get_attribute("innerText"))
    size = unicodedata.normalize("NFKD", card.find_element(By.CSS_SELECTOR, size_css).get_attribute("innerText"))
    price = unicodedata.normalize("NFKD", card.find_element(By.CSS_SELECTOR, price_css).get_attribute("innerText"))
    rate = unicodedata.normalize("NFKD", card.find_element(By.CSS_SELECTOR, rate_css).get_attribute("innerText"))
    return SubscriptionInfo(
        name=name,
        size=size,
        price=price,
        rate=rate
    )


def web_element_wait_clickable(element, locator, timeout=2):
    return WebDriverWait(element, timeout).until(ec.element_to_be_clickable(locator))


def web_element_wait_located(element, locator):
    return WebDriverWait(element, 2).until(ec.presence_of_element_located(locator))
