from configs.setting import Setting

from .base import Page


class AdminClientsPage(Page):
    URL = f'{Setting().app_domain}/clients'

# TODO: Remove
class AdminClientsPage1(Page):
    URL = f'{Setting().app_domain}/browser'
