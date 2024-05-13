from unittest import TestCase

from webapp.testcases.log_in_log_out import LogInLogOut


class TestLogInLogOut(LogInLogOut, TestCase):
    def __init__(self, *arg, **kwargs):
        LogInLogOut.__init__(self, machine=None, independent=False)
        TestCase.__init__(self, *arg, **kwargs)
