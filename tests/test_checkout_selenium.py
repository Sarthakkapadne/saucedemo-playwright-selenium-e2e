"""
Selenium Checkout Test Suite (3 Test Cases).
Validates end-to-end checkout, input validations, and cancellation handling via WebDriver.
"""
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.selenium_pages.login_selenium_page import LoginSeleniumPage
from pages.selenium_pages.inventory_selenium_page import InventorySeleniumPage
from pages.selenium_pages.cart_selenium_page import CartSeleniumPage
from pages.selenium_pages.checkout_selenium_page import (
    CheckoutStepOneSeleniumPage,
    CheckoutStepTwoSeleniumPage,
    CheckoutCompleteSeleniumPage,
)
from config.settings import settings


@allure.feature("Checkout & Payment Processing")
@allure.story("Selenium Order Processing Flows")
@pytest.mark.selenium
class TestCheckoutSelenium:

    @pytest.fixture(autouse=True)
    def setup_logged_in(self, selenium_driver):
        login_page = LoginSeleniumPage(selenium_driver)
        login_page.login(settings.STANDARD_USER, settings.DEFAULT_PASSWORD)
        self.inventory_page = InventorySeleniumPage(selenium_driver)
        self.cart_page = CartSeleniumPage(selenium_driver)
        self.step_one = CheckoutStepOneSeleniumPage(selenium_driver)
        self.step_two = CheckoutStepTwoSeleniumPage(selenium_driver)
        self.complete_page = CheckoutCompleteSeleniumPage(selenium_driver)

    @allure.title("TC-E2E-23: Selenium Full Checkout Transaction Completion")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_selenium_complete_checkout(self, selenium_driver):
        with allure.step("Add product to cart and proceed to checkout"):
            self.inventory_page.add_first_item_to_cart()
            self.inventory_page.open_cart()
            self.cart_page.checkout()

        with allure.step("Submit checkout step one details"):
            self.step_one.fill_information(first_name="Sarthak", last_name="Kapadne", postal_code="411001")
            self.step_one.click_continue()

        with allure.step("Verify step two calculations and finish order"):
            WebDriverWait(selenium_driver, 10).until(EC.url_contains("checkout-step-two.html"))
            subtotal = self.step_two.get_subtotal()
            tax = self.step_two.get_tax()
            total = self.step_two.get_total()
            assert round(subtotal + tax, 2) == round(total, 2)
            self.step_two.click_finish()

        with allure.step("Assert order complete message"):
            WebDriverWait(selenium_driver, 10).until(EC.url_contains("checkout-complete.html"))
            assert self.complete_page.is_order_successful()

    @allure.title("TC-E2E-24: Selenium Missing Last Name Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_selenium_missing_lastname_validation(self, selenium_driver):
        with allure.step("Navigate to checkout"):
            self.inventory_page.add_first_item_to_cart()
            self.inventory_page.open_cart()
            self.cart_page.checkout()

        with allure.step("Submit without last name"):
            self.step_one.fill_information(first_name="Sarthak", last_name="", postal_code="411001")
            self.step_one.click_continue()

        with allure.step("Assert error message for last name"):
            assert "Error: Last Name is required" in self.step_one.get_error_message()

    @allure.title("TC-E2E-25: Selenium Cancel at Checkout Step Two Returns to Inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_selenium_cancel_at_step_two(self, selenium_driver):
        with allure.step("Navigate to checkout step two overview"):
            self.inventory_page.add_first_item_to_cart()
            self.inventory_page.open_cart()
            self.cart_page.checkout()
            self.step_one.fill_information(first_name="Sarthak", last_name="Kapadne", postal_code="411001")
            self.step_one.click_continue()

        with allure.step("Click Cancel button at Step Two"):
            WebDriverWait(selenium_driver, 10).until(EC.url_contains("checkout-step-two.html"))
            self.step_two.click_cancel()

        with allure.step("Assert returned to products inventory"):
            WebDriverWait(selenium_driver, 10).until(EC.url_contains("inventory.html"))
            assert self.inventory_page.get_items_count() == 6
