"""
Product Detail Page Object.
"""
from pages.base_page import BasePage


class ItemDetailPage(BasePage):
    ITEM_NAME = ".inventory_details_name"
    ITEM_PRICE = ".inventory_details_price"
    ITEM_DESC = ".inventory_details_desc"
    ADD_TO_CART_BTN = "button[id^='add-to-cart']"
    REMOVE_BTN = "button[id^='remove']"
    BACK_BUTTON = "[data-test='back-to-products']"
    CART_BADGE = ".shopping_cart_badge"

    def get_name(self) -> str:
        return self.get_text(self.ITEM_NAME)

    def get_price(self) -> float:
        text = self.get_text(self.ITEM_PRICE)
        return float(text.replace("$", "").strip())

    def get_description(self) -> str:
        return self.get_text(self.ITEM_DESC)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def remove_from_cart(self):
        self.click(self.REMOVE_BTN)

    def back_to_products(self):
        self.click(self.BACK_BUTTON)
