from .common import TestCommon


class TestSession(TestCommon):
    def test_session(self):
        self.login()
        self.click(".o_user_menu > a[role='button']")
        self.wait_for_text_visible("Log out", "[data-menu='logout']")
        self.click("[data-menu='logout']")
