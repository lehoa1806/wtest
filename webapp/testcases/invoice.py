import os
import re
from time import sleep

from configs import ROOT_DIR
from configs.setting import Setting
from robot.elements.button import Button
from webapp.testcases.base import BaseTestCase


class Invoice(BaseTestCase):
    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user('user_with_invoice')
    def test_user_view_invoice(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.view_invoice()

    @BaseTestCase.machine
    @BaseTestCase.require_login_with_user('user_with_invoice')
    def test_user_view_and_download_invoice(self):
        self.robot.load_url(f'{Setting().app_domain}/settings/billing')
        self.download_invoice(self.view_invoice())

    def view_invoice(self):
        btn_show_invoices = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector='//button[@type="button" and text()="Invoices"]'
        )
        btn_show_invoices.click()

        self.robot.find_element_by_xpath(
            xpath='//div[contains(@class, "text-foreground") and text()="Date"]'
        )
        self.robot.find_element_by_xpath(
            xpath='//div[contains(@class, "text-foreground") and text()="Plan"]'
        )
        self.robot.find_element_by_xpath(
            xpath='//div[contains(@class, "text-foreground") and text()="Amount"]'
        )
        self.robot.find_element_by_xpath(
            xpath='//div[contains(@class, "text-foreground") and text()="Status"]'
        )

        btn_view_invoice = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector='//button[@type="button" and text()="View invoice"][1]'
        )

        btn_view_invoice.click()

        self.robot.find_element_by_xpath(
            xpath='//span[@role="presentation" and starts-with(text(), "Receipt #")]'
        )

        self.robot.find_element_by_xpath(
            xpath='//span[@role="presentation" and text()="AMOUNT PAID"]'
        )

        self.robot.find_element_by_xpath(
            xpath='//span[@role="presentation" and text()="DATE PAID"]'
        )

        self.robot.find_element_by_xpath(
            xpath='//span[@role="presentation" and text()="PAYMENT METHOD"]'
        )

        self.robot.find_element_by_xpath(
            xpath='//span[@role="presentation" and text()="SUMMARY"]'
        )

        nda_statement = '//p[text()="All of your credit card details and data is secured."]'

        self.robot.find_element_by_xpath(
            xpath=nda_statement
        )

        btn_download_xpath = f'({nda_statement}/../following-sibling::*[1]//button)[1]'
        btn_download = Button.load_button_by_xpath_selector(
            parent=self.robot.browser,
            xpath_selector=btn_download_xpath
        )
        return btn_download

    def download_invoice(self, btn_download: Button):
        btn_download.click()
        sleep(3)

        download_folder = f'{ROOT_DIR}/logs'
        file_name = r'Invoice_Opensend_.*.pdf'
        file_found = False
        for file in os.listdir(download_folder):
            if re.match(file_name, file):
                file_found = True
                break
        assert file_found, f'File {file_name} not found in {download_folder}'

