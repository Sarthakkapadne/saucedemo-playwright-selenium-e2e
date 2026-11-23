"""
Selenium Checkout Page Objects.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.selenium_pages.base_selenium_page import BaseSeleniumPage


class CheckoutStepOneSeleniumPage(BaseSeleniumPage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_information(self, first_name: str = "", last_name: str = "", postal_code: str = ""):
        if first_name:
            self.type_text(*self.FIRST_NAME_INPUT, first_name)
        if last_name:
            self.type_text(*self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.type_text(*self.POSTAL_CODE_INPUT, postal_code)
        return self

    def click_continue(self):
        self.click(*self.CONTINUE_BUTTON)

    def click_cancel(self):
        self.click(*self.CANCEL_BUTTON)
        self.wait.until(EC.url_contains("/cart.html"))

    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_CONTAINER)


class CheckoutStepTwoSeleniumPage(BaseSeleniumPage):
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    def get_subtotal(self) -> float:
        text = self.get_text(*self.SUBTOTAL_LABEL)
        return float(text.split("$")[-1].strip())

    def get_tax(self) -> float:
        text = self.get_text(*self.TAX_LABEL)
        return float(text.split("$")[-1].strip())

    def get_total(self) -> float:
        text = self.get_text(*self.TOTAL_LABEL)
        return float(text.split("$")[-1].strip())

    def click_finish(self):
        self.click(*self.FINISH_BUTTON)
        self.wait.until(EC.url_contains("checkout-complete.html"))

    def click_cancel(self):
        self.click(*self.CANCEL_BUTTON)
        self.wait.until(EC.url_contains("/inventory.html"))


class CheckoutCompleteSeleniumPage(BaseSeleniumPage):
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BTN = (By.ID, "back-to-products")

    def get_header(self) -> str:
        return self.get_text(*self.COMPLETE_HEADER)

    def is_order_successful(self) -> bool:
        return "thank you for your order" in self.get_header().lower()
