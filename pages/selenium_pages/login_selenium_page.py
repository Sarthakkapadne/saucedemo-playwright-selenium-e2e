"""
Selenium Login Page Object.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.selenium_pages.base_selenium_page import BaseSeleniumPage


class LoginSeleniumPage(BaseSeleniumPage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")

    def navigate(self):
        return self.open("")

    def enter_username(self, username: str):
        self.type_text(*self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.type_text(*self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(*self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.navigate()
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()
        if username and password and "wrong" not in password and "locked" not in username:
            try:
                self.wait.until(EC.url_contains("/inventory.html"))
            except Exception:
                pass

    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        return self.is_visible(*self.ERROR_CONTAINER)
