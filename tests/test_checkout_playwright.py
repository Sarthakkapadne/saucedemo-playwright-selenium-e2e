"""
Playwright Checkout & Order Processing Test Suite (4 Test Cases).
Validates complete purchase transaction, subtotal/tax price arithmetic, and input validations.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from config.settings import settings


@allure.feature("Checkout & Payment Processing")
@allure.story("Order Completion and Validation Flows")
@pytest.mark.playwright
class TestCheckoutPlaywright:

    @pytest.fixture(autouse=True)
    def setup_logged_in(self, page):
        login_page = LoginPage(page)
        login_page.login(settings.STANDARD_USER, settings.DEFAULT_PASSWORD)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        self.step_one = CheckoutStepOnePage(page)
        self.step_two = CheckoutStepTwoPage(page)
        self.complete_page = CheckoutCompletePage(page)

    @allure.title("TC-E2E-12: Full End-to-End Checkout Flow with Price & Tax Verification")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.e2e
    def test_e2e_checkout_success(self, page):
        with allure.step("Add items to cart and navigate to cart"):
            self.inventory_page.add_item_by_name("Sauce Labs Backpack")
            self.inventory_page.add_item_by_name("Sauce Labs Bike Light")
            self.inventory_page.open_cart()
            assert self.cart_page.get_cart_items_count() == 2

        with allure.step("Proceed to checkout step one and enter customer details"):
            self.cart_page.checkout()
            self.step_one.fill_information(
                first_name="Sarthak",
                last_name="Kapadne",
                postal_code="411001",
            )
            self.step_one.click_continue()

        with allure.step("Verify checkout overview calculations (Subtotal + Tax = Total)"):
            assert "/checkout-step-two.html" in page.url
            subtotal = self.step_two.get_subtotal()
            tax = self.step_two.get_tax()
            total = self.step_two.get_total()
            assert subtotal == 39.98  # $29.99 + $9.99
            assert round(subtotal + tax, 2) == round(total, 2)

        with allure.step("Complete order and verify confirmation message"):
            self.step_two.click_finish()
            assert "/checkout-complete.html" in page.url
            assert self.complete_page.is_order_successful()
            assert "Thank you for your order!" in self.complete_page.get_header()

    @allure.title("TC-E2E-13: Missing first name validation on checkout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_step_one_empty_firstname(self, page):
        with allure.step("Navigate to checkout step one"):
            self.inventory_page.add_item_by_name("Sauce Labs Backpack")
            self.inventory_page.open_cart()
            self.cart_page.checkout()

        with allure.step("Submit form without first name"):
            self.step_one.fill_information(first_name="", last_name="Kapadne", postal_code="411001")
            self.step_one.click_continue()

        with allure.step("Assert First Name is required error"):
            assert "Error: First Name is required" in self.step_one.get_error_message()

    @allure.title("TC-E2E-14: Missing postal code validation on checkout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_step_one_empty_postal_code(self, page):
        with allure.step("Navigate to checkout step one"):
            self.inventory_page.add_item_by_name("Sauce Labs Backpack")
            self.inventory_page.open_cart()
            self.cart_page.checkout()

        with allure.step("Submit form without postal code"):
            self.step_one.fill_information(first_name="Sarthak", last_name="Kapadne", postal_code="")
            self.step_one.click_continue()

        with allure.step("Assert Postal Code is required error"):
            assert "Error: Postal Code is required" in self.step_one.get_error_message()

    @allure.title("TC-E2E-15: Cancel checkout returns user to cart with items intact")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_cancel_flow(self, page):
        with allure.step("Add item and proceed to checkout"):
            self.inventory_page.add_item_by_name("Sauce Labs Bolt T-Shirt")
            self.inventory_page.open_cart()
            self.cart_page.checkout()

        with allure.step("Cancel checkout step one"):
            self.step_one.click_cancel()

        with allure.step("Verify returned to cart page and item is still present"):
            assert "/cart.html" in page.url
            assert self.cart_page.get_cart_items_count() == 1
            assert "Sauce Labs Bolt T-Shirt" in self.cart_page.get_cart_item_names()
