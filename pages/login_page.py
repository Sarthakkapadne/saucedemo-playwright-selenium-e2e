"""
Login Page Object for SauceDemo.
"""
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_CONTAINER = "[data-test='error']"
    ERROR_BUTTON = ".error-button"

    def navigate(self):
        return self.open("")

    def enter_username(self, username: str):
        self.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.navigate()
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_CONTAINER)

    def close_error(self):
        if self.is_visible(self.ERROR_BUTTON):
            self.click(self.ERROR_BUTTON)
