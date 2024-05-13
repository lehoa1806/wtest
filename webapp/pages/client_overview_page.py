from configs.setting import Setting

from .base import Page


class ClientOverviewPage(Page):
    URL = f'{Setting().app_domain}/overview'
