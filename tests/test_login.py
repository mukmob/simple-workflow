import logging

from seleniumbase import BaseCase

logger = logging.getLogger(__name__)


class OdooLoginTest(BaseCase):
    def test_login(self):
        self.open("http://localhost:8069")
        self.type("#login", "admin")
        self.type("#password", "admin")
        self.click('button[type="submit"]')
        logger.info(self.get_page_source())
        self.assert_text("Odoo", "title")
