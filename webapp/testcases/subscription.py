import logging
import unicodedata
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from configs.setting import Setting
from selenium.webdriver.support import expected_conditions as ec
from webapp.pages.subscription import all_subscriptions
from webapp.testcases.base import BaseTestCase


class Subscription(BaseTestCase):
    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user('new_user')
    def test_new_user_show_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.show_subscriptions(is_new_user=True)

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user()
    def test_old_user_show_subscription(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/subscription')
        self.show_subscriptions()

    def show_subscriptions(self, is_new_user: bool = False) -> List[WebElement]:

        button_show_subscription_xpath = '//button[text()="Show subscription plans"]' if is_new_user \
            else '//button[text()="See all plans"]'

        subscript_card_xpath = (
            '//div[contains(@class, "bg-card") and contains(@class, "@container")]'
        )

        subscribe_button_xpath = (
            '//button[@type="button" and text()="Subscribe"]'
        )

        show_sub_btn = self.robot.find_element_by_xpath(
            xpath=button_show_subscription_xpath
        )
        show_sub_btn.click()

        subscription_cards = self.robot.find_elements_by_xpath(
            xpath=subscript_card_xpath
        )
        assert len(subscription_cards) == 10

        subs = []
        for c in subscription_cards:
            s = extract_subscription_info(self.robot, c)
            subs.append(s)
        logging.info(subs)
        for s in subs:
            diff_assert(all_subscriptions[s["name"]]["price"], s["price"])
            diff_assert(all_subscriptions[s["name"]]["size"], s["size"])
            diff_assert(all_subscriptions[s["name"]]["rate"], s["rate"])

        return subscription_cards

    def buy_subscription(self, sub: WebElement, sub_info) -> None:
        sub.find_element(By.XPATH, '//button[text()="Subscribe"]').click()

        sub_name_xpath = (
            f'//h4[text()={sub_info["name"].string.lower().capitalize() + " plan"}]'
        )

        btn_next_xpath = '//button[text()="Next"]'

        sub_name = self.robot.find_element_by_xpath(xpath=sub_name_xpath)
        parent = sub_name.find_element(By.XPATH, '..//..')


def diff_assert(a, b):
    if a != b:
        logging.error(f'{a} != {b}')
        raise AssertionError


class SubscriptionInfo(dict):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self[k] = v


def extract_subscription_info(robot, card) -> SubscriptionInfo:
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


def web_element_wait(element, locator):
    return WebDriverWait(element, 2).until(ec.visibility_of_element_located(locator))
