import logging

from seleniumbase import BaseCase

logger = logging.getLogger(__name__)


class OdooLoginTest(BaseCase):
    def test_login(self):
        logging.info("test_login")
        self.open("http://localhost:8069")
        self.type("#login", "user@example.com")
        self.type("#password", "bitnami")
        self.click('button[type="submit"]')
        logger.info(self.get_page_source())
        self.assert_element("[data-hotkey='h']")
