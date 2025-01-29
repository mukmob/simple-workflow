import logging
import time
import os

from selenium.webdriver.common.keys import Keys
from seleniumbase import BaseCase
from seleniumbase.common.exceptions import (
    ElementNotVisibleException,
    NoSuchElementException,
)

BACK_BUTTON = "[accesskey='b']"
CREATE_BUTTON = "[accesskey='c']"
DASHBOARD_BUTTON = "[accesskey='a']"
EDIT_BUTTON = "[accesskey='e']"
LIST_VIEW_BUTTON = "[accesskey='l']"
SAVE_BUTTON = "[accesskey='s']"

logger = logging.getLogger(__name__)
test_data = {
    "_comment_a": "Login data here..",
    "base_url": os.getenv("BASE_URL", "http://localhost:8069"),
    "login_credentials": {
        "admin": {
            "login": os.getenv("ODOO_EMAIL", "admin"),
            "password": os.getenv("ODOO_PASSWORD", "admin"),
        },
        "test_user": {
            "login": os.getenv("TEST_USER_EMAIL", "test_user"),
            "password": os.getenv("TEST_USER_PASSWORD", "test_user"),
        },
    },
}


class LoginException(Exception):
    pass


class GeneralSettingsException(Exception):
    pass


class TestCommon(BaseCase):
    # /***************************** Helper functions  ***************************/

    def _scroll_to_field(self, field_name):
        possible_selectors = [
            f"#{field_name}",
            f"input[name='{field_name}']",
            f"input[name='{field_name}']:last-of-type",
            f"div[name='{field_name}'] input",
            f"div[name='{field_name}']",
        ]
        for selector in possible_selectors:
            try:
                self.scroll_to(selector, timeout=0.5)
                return selector
            except (NoSuchElementException, ElementNotVisibleException):
                pass
        raise NoSuchElementException(f"Field {field_name} not found on the page")

    def go_to_dashboard(self):
        dashboard_menu = self.find_element(DASHBOARD_BUTTON)
        showing = dashboard_menu.get_attribute("aria-expanded") == "true"
        if not showing:
            dashboard_menu.click()

    def wait_for_breadcrumb(self, breadcrumb):
        self.wait_for_text_visible(
            breadcrumb, "ol[role='navigation'] > .breadcrumb-item", timeout=20
        )

    def click_tab(self, tab_name):
        self.click(f"//a[@role='tab' and text()='{tab_name}']")

    def go_to_settings_menu(self):
        self.go_to_dashboard()
        self.click("[data-menu-xmlid='base.menu_administration']")
        self.wait_for_text_visible("Settings", ".o_main_navbar > a[role='button']")

    def click_back_button(self):
        self.click(BACK_BUTTON)

    def click_create_button(self):
        self.click(CREATE_BUTTON)
        self.wait_for_element_clickable(SAVE_BUTTON)

    def click_edit_button(self):
        self.click(EDIT_BUTTON)

    def click_save_button(self):
        self.click(SAVE_BUTTON)
        self.wait_for_element_clickable(EDIT_BUTTON, timeout=20)

    def click_list_view(self):
        if self.is_element_visible(LIST_VIEW_BUTTON):
            self.click(LIST_VIEW_BUTTON)

    def search_record(self, search_string, timeout=1, list_view=True):
        if list_view:
            self.click_list_view()
        searchbox = "input[role='searchbox']"
        self.type(searchbox, search_string)
        self.send_keys(searchbox, Keys.ENTER)
        try:
            self.wait_for_element_visible(
                f"td[title='{search_string}']", timeout=timeout
            )
            return True
        except NoSuchElementException:
            return False

    def click_record(self, record_name):
        self.click(f"td[title='{record_name}']")

    def create_record(self, data):
        self.click_create_button()
        for field, value in data.items():
            self.set_field_value(field, value)
        self.click(SAVE_BUTTON)
        self.wait_for_element_clickable(EDIT_BUTTON)

    def edit_record(self, data):
        self.click_edit_button()
        for field, value in data.items():
            self.set_field_value(field, value)
        self.click(SAVE_BUTTON)
        self.wait_for_element_clickable(EDIT_BUTTON)

    def set_field_value(self, field_name, value, clear_input=True, clear_wait_time=1):
        input_field = self._scroll_to_field(field_name)
        self.click(input_field)
        if clear_input:
            self.clear(input_field)
            self.wait(clear_wait_time)
        self.add_text(input_field, value)
        self.wait(1)
        self.send_keys(input_field, Keys.ENTER)

    def clear_field(self, field_name):
        input_field = self._scroll_to_field(field_name)
        self.clear(input_field)

    def clear_many2many_tags_field(self, field_name):
        delete_buttons = self.find_elements(
            f"//div[@name='{field_name}']//a[contains(@class, 'o_delete')]"
        )
        for button in delete_buttons:
            button.click()

    def set_select_field_value(self, field_name, value):
        selector = f"select[name='{field_name}']"
        self.scroll_to(selector, timeout=0.5)
        self.select_option_by_text(selector, value)

    def check_field(self, field_name):
        self.check_if_unchecked(f"div[name='{field_name}'] .custom-control-input")

    # /*****************************  Odoo functionality  ***************************/
    def login(self, user="admin", max_attempts=1, wait_time=5):
        self.maximize_window()
        self.open(test_data["base_url"] + "/web/login?debug=1")
        self.assert_element("form")
        self.type('input[name="login"]', test_data["login_credentials"][user]["login"])
        self.type(
            'input[name="password"]', test_data["login_credentials"][user]["password"]
        )
        self.click("button[type='submit'].btn.btn-primary.btn-block")
        for attempt in range(max_attempts):
            try:
                logger.info(f"Login attempt {attempt + 1}")
                logger.info(test_data["login_credentials"][user]["login"])
                logger.info(self.get_page_title())
                logger.info(self.get_current_url())
                logger.info(self.get_page_source())
                self.wait_for_element_visible(DASHBOARD_BUTTON, timeout=300)
                break
            except Exception as e:
                if attempt >= max_attempts - 1:
                    raise LoginException(
                        f"Login failed after {max_attempts} attempts: {str(e)}"
                    ) from e
                self.refresh_page()
                time.sleep(wait_time)
        self.go_to_dashboard()

    def add_user_to_group(self, login, group_name):
        self.go_to_settings_menu()
        self.wait(1)
        self.click('[data-menu-xmlid="base.menu_users"]')
        self.click('[data-menu-xmlid="base.menu_action_res_groups"]')
        self.click_record(group_name)
        self.click_edit_button()
        self.click("[name='users'] a")
        self.assert_element(".modal-content")
        self.search_record(login)
        user_row_selector = f"td[title='{login}']"
        if self.is_element_visible(f".modal-dialog {user_row_selector}"):
            self.click(user_row_selector)
            self.click_save_button()
        else:
            self.click("div.modal-dialog button.o_form_button_cancel")

    def switch_to_company(self, company_name):
        self.click(".o_switch_company_menu")
        self.click(f"//span[normalize-space(text())='{company_name}']")
        self.wait(2)
