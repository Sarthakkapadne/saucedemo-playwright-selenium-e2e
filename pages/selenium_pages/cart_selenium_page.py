"""
Selenium Cart Page Object.
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.selenium_pages.base_selenium_page import BaseSeleniumPage


class CartSeleniumPage(BaseSeleniumPage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CONTINUE_SHOPPING_BTN = (By.CSS_SELECTOR, "[data-test='continue-shopping']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")

    def get_cart_items_count(self) -> int:
        return len(self.find_all(*self.CART_ITEM))

    def get_cart_item_names(self) -> List[str]:
        elements = self.find_all(*self.ITEM_NAME)
        return [e.text.strip() for e in elements]

    def remove_first_item(self):
        remove_btn = (By.CSS_SELECTOR, "button[id^='remove']")
        self.click(*remove_btn)

    def continue_shopping(self):
        self.click(*self.CONTINUE_SHOPPING_BTN)
        self.wait.until(EC.url_contains("/inventory.html"))

    def checkout(self):
        self.click(*self.CHECKOUT_BUTTON)
        self.wait.until(EC.url_contains("checkout-step-one.html"))
