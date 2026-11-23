"""
Checkout Step One, Two, and Complete Page Objects.
"""
from typing import List
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_CONTAINER = "[data-test='error']"

    def fill_information(self, first_name: str = "", last_name: str = "", postal_code: str = ""):
        if first_name:
            self.fill(self.FIRST_NAME_INPUT, first_name)
        if last_name:
            self.fill(self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.fill(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        self.page.wait_for_url("**/cart.html*", timeout=5000)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_CONTAINER)


class CheckoutStepTwoPage(BasePage):
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    FINISH_BUTTON = "[data-test='finish']"
    CANCEL_BUTTON = "[data-test='cancel']"

    def get_item_names(self) -> List[str]:
        return self.page.locator(self.ITEM_NAME).all_text_contents()

    def get_subtotal(self) -> float:
        # Format: "Item total: $29.99"
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.split("$")[-1].strip())

    def get_tax(self) -> float:
        # Format: "Tax: $2.40"
        text = self.get_text(self.TAX_LABEL)
        return float(text.split("$")[-1].strip())

    def get_total(self) -> float:
        # Format: "Total: $32.39"
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.split("$")[-1].strip())

    def click_finish(self):
        self.click(self.FINISH_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BTN = "[data-test='back-to-products']"
    PONY_EXPRESS_IMG = ".pony_express"

    def get_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_text_content(self) -> str:
        return self.get_text(self.COMPLETE_TEXT)

    def is_order_successful(self) -> bool:
        return "thank you for your order" in self.get_header().lower()

    def back_home(self):
        self.click(self.BACK_HOME_BTN)
