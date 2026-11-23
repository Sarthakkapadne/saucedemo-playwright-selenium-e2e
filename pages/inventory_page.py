"""
Inventory / Products Catalog Page Object.
"""
from typing import List
from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_DESC = ".inventory_item_desc"
    ADD_TO_CART_BTN = "button[id^='add-to-cart']"
    REMOVE_BTN = "button[id^='remove']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    BURGER_MENU_BTN = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_APP_STATE_LINK = "#reset_sidebar_link"

    def is_loaded(self) -> bool:
        try:
            self.page.wait_for_selector(self.INVENTORY_CONTAINER, timeout=5000)
            return True
        except Exception:
            return False

    def get_item_count(self) -> int:
        self.page.wait_for_selector(self.INVENTORY_ITEM)
        return self.page.locator(self.INVENTORY_ITEM).count()

    def get_item_names(self) -> List[str]:
        self.page.wait_for_selector(self.ITEM_NAME)
        return self.page.locator(self.ITEM_NAME).all_text_contents()

    def get_item_prices(self) -> List[float]:
        self.page.wait_for_selector(self.ITEM_PRICE)
        price_texts = self.page.locator(self.ITEM_PRICE).all_text_contents()
        return [float(p.replace("$", "").strip()) for p in price_texts]

    def add_item_by_name(self, product_name: str):
        item_card = self.page.locator(self.INVENTORY_ITEM).filter(has_text=product_name)
        item_card.locator("button").click()

    def remove_item_by_name(self, product_name: str):
        item_card = self.page.locator(self.INVENTORY_ITEM).filter(has_text=product_name)
        item_card.locator("button").click()

    def add_first_item(self):
        self.page.locator(self.ADD_TO_CART_BTN).first.click()

    def get_cart_badge_count(self) -> int:
        if not self.is_cart_badge_present():
            return 0
        text = self.get_text(self.CART_BADGE)
        return int(text) if text.isdigit() else 0

    def is_cart_badge_present(self) -> bool:
        return self.is_visible(self.CART_BADGE, timeout=2000)

    def open_cart(self):
        self.click(self.CART_LINK)
        self.page.wait_for_url("**/cart.html*", timeout=5000)

    def select_sort(self, sort_value: str):
        # Options: 'az', 'za', 'lohi', 'hilo'
        self.page.select_option(self.SORT_DROPDOWN, sort_value)

    def click_item_title(self, product_name: str):
        self.page.locator(self.ITEM_NAME).filter(has_text=product_name).click()

    def logout(self):
        self.click(self.BURGER_MENU_BTN)
        self.page.wait_for_selector(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)
