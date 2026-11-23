"""
Selenium Inventory Page Object.
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.selenium_pages.base_selenium_page import BaseSeleniumPage


class InventorySeleniumPage(BaseSeleniumPage):
    INVENTORY_CONTAINER = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    def get_items_count(self) -> int:
        return len(self.find_all(*self.INVENTORY_ITEM))

    def get_item_names(self) -> List[str]:
        elements = self.find_all(*self.ITEM_NAME)
        return [e.text.strip() for e in elements]

    def add_first_item_to_cart(self):
        btn = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
        self.click(*btn)

    def add_item_by_name(self, product_name: str):
        items = self.find_all(*self.INVENTORY_ITEM)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip() == product_name:
                item.find_element(By.CSS_SELECTOR, "button").click()
                return

    def get_cart_badge_count(self) -> int:
        if not self.is_visible(*self.CART_BADGE, timeout=2):
            return 0
        text = self.get_text(*self.CART_BADGE)
        return int(text) if text.isdigit() else 0

    def open_cart(self):
        self.click(*self.CART_LINK)

    def select_sort(self, sort_value: str):
        dropdown = Select(self.find(*self.SORT_DROPDOWN))
        dropdown.select_by_value(sort_value)
