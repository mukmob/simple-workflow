import logging

from seleniumbase import BaseCase

logger = logging.getLogger(__name__)


class OdooLoginTest(BaseCase):
    def test_login(self):
        logging.info("test_login")
        self.open("http://localhost:8069/web/login")
        self.type("#login", "user@example.com")
        self.type("#password", "bitnami")
        self.click('button[type="submit"]')
        self.assert_element("[accesskey='h']")
