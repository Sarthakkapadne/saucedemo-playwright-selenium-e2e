"""
Cart Page Object.
"""
from typing import List
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = "button[id^='remove']"
    CONTINUE_SHOPPING_BTN = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def get_cart_items_count(self) -> int:
        try:
            self.page.wait_for_selector(self.CART_ITEM, timeout=3000)
            return self.page.locator(self.CART_ITEM).count()
        except Exception:
            return 0

    def get_cart_item_names(self) -> List[str]:
        try:
            self.page.wait_for_selector(self.ITEM_NAME, timeout=3000)
            return self.page.locator(self.ITEM_NAME).all_text_contents()
        except Exception:
            return []

    def remove_item_by_name(self, product_name: str):
        cart_row = self.page.locator(self.CART_ITEM).filter(has_text=product_name)
        cart_row.locator(self.REMOVE_BUTTON).click()

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BTN)
        self.page.wait_for_url("**/inventory.html*", timeout=5000)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.page.wait_for_url("**/checkout-step-one.html*", timeout=5000)
