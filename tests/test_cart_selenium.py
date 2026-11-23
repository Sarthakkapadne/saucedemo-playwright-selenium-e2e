"""
Selenium Cart Operations Test Suite (3 Test Cases).
Validates item additions, cart badge counters, removals, and continue shopping navigation.
"""
import pytest
import allure
from pages.selenium_pages.login_selenium_page import LoginSeleniumPage
from pages.selenium_pages.inventory_selenium_page import InventorySeleniumPage
from pages.selenium_pages.cart_selenium_page import CartSeleniumPage
from config.settings import settings


@allure.feature("Product Catalog & Cart Management")
@allure.story("Selenium Cart Management Flows")
@pytest.mark.selenium
class TestCartSelenium:

    @pytest.fixture(autouse=True)
    def setup_logged_in(self, selenium_driver):
        login_page = LoginSeleniumPage(selenium_driver)
        login_page.login(settings.STANDARD_USER, settings.DEFAULT_PASSWORD)
        self.inventory_page = InventorySeleniumPage(selenium_driver)
        self.cart_page = CartSeleniumPage(selenium_driver)

    @allure.title("TC-E2E-20: Selenium Add Item to Cart and Verify Badge Count")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_selenium_add_item_and_verify_badge(self, selenium_driver):
        with allure.step("Add first item from catalog"):
            self.inventory_page.add_first_item_to_cart()

        with allure.step("Assert cart badge displays '1'"):
            assert self.inventory_page.get_cart_badge_count() == 1

    @allure.title("TC-E2E-21: Selenium Remove Item from Cart Page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_selenium_remove_item_from_cart_page(self, selenium_driver):
        with allure.step("Add item, navigate to cart, and verify item in cart"):
            self.inventory_page.add_first_item_to_cart()
            self.inventory_page.open_cart()
            assert self.cart_page.get_cart_items_count() == 1

        with allure.step("Remove item from cart"):
            self.cart_page.remove_first_item()

        with allure.step("Assert cart is now empty"):
            assert self.cart_page.get_cart_items_count() == 0

    @allure.title("TC-E2E-22: Selenium Continue Shopping Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_selenium_continue_shopping(self, selenium_driver):
        with allure.step("Open cart and click Continue Shopping"):
            self.inventory_page.open_cart()
            assert "/cart.html" in selenium_driver.current_url
            self.cart_page.continue_shopping()

        with allure.step("Assert returned to inventory page"):
            assert "/inventory.html" in selenium_driver.current_url
            assert self.inventory_page.get_items_count() == 6
