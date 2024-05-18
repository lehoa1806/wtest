import pytest

from webapp.testcases.invoice import Invoice
from webapp.testcases.log_in_log_out import LogInLogOut
from webapp.testcases.payment import Payment
from webapp.testcases.subscription import Subscription


@pytest.mark.usefixtures("machine")
class TestSuite:
    def test_user_logs_in_successfully(self, machine):
        LogInLogOut(machine=machine).test_user_logs_in_successfully()

    def test_user_logs_out_successfully(self, machine):
        LogInLogOut(machine=machine).test_user_logs_out_successfully()

    def test_user_add_payment(self, machine):
        Payment(machine=machine).test_user_add_payment()

    def test_user_remove_primary_payment(self, machine):
        Payment(machine=machine).test_user_remove_primary_payment()

    def test_user_remove_secondary_payment(self, machine):
        Payment(machine=machine).test_user_remove_secondary_payment()

    def test_user_make_primary_payment(self, machine):
        Payment(machine=machine).test_user_make_primary_payment()

    def test_user_view_invoice(self, machine):
        Invoice(machine=machine).test_user_view_invoice()

    def test_user_view_and_download_invoice(self, machine):
        Invoice(machine=machine).test_user_view_and_download_invoice()

    def test_user_view_subscription(self, machine):
        Subscription(machine=machine).test_new_user_view_subscription()

    def test_user_buy_subscription(self, machine):
        Subscription(machine=machine).test_user_buy_subscription()

    def test_user_cancel_subscription(self, machine):
        Subscription(machine=machine).test_user_cancel_subscription()

    def test_user_cancel_and_keep_current_subscription(self, machine):
        Subscription(machine=machine).test_user_cancel_and_keep_current_subscription()

    def test_user_resubscribe_subscription(self, machine):
        Subscription(machine=machine).test_user_resubscribe_subscription()
