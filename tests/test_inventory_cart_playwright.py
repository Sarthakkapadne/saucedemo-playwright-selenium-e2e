"""
Playwright Inventory & Cart Operations Test Suite (6 Test Cases).
Validates product sorting, catalog actions, cart persistence, and item details.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.item_detail_page import ItemDetailPage
from config.settings import settings


@allure.feature("Product Catalog & Cart Management")
@allure.story("Catalog Sorting and Cart Operations")
@pytest.mark.playwright
class TestInventoryCartPlaywright:

    @pytest.fixture(autouse=True)
    def setup_logged_in(self, page):
        login_page = LoginPage(page)
        login_page.login(settings.STANDARD_USER, settings.DEFAULT_PASSWORD)
        self.inventory_page = InventoryPage(page)

    @allure.title("TC-E2E-06: Adding multiple items accurately updates cart badge counter")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_multiple_items_updates_badge(self, page):
        with allure.step("Add two distinct items to cart"):
            self.inventory_page.add_item_by_name("Sauce Labs Backpack")
            self.inventory_page.add_item_by_name("Sauce Labs Bike Light")

        with allure.step("Assert cart badge count is 2"):
            assert self.inventory_page.get_cart_badge_count() == 2

    @allure.title("TC-E2E-07: Removing item from catalog clears cart badge")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_remove_item_from_catalog(self, page):
        with allure.step("Add an item then remove it from catalog"):
            self.inventory_page.add_item_by_name("Sauce Labs Bolt T-Shirt")
            assert self.inventory_page.get_cart_badge_count() == 1
            self.inventory_page.remove_item_by_name("Sauce Labs Bolt T-Shirt")

        with allure.step("Assert cart badge is no longer displayed"):
            assert not self.inventory_page.is_cart_badge_present()

    @allure.title("TC-E2E-08: Sort products by price (low to high)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_price_low_to_high(self, page):
        with allure.step("Select Price (low to high) sort option"):
            self.inventory_page.select_sort("lohi")

        with allure.step("Verify prices are strictly ascending"):
            prices = self.inventory_page.get_item_prices()
            assert prices == sorted(prices)
            assert prices[0] <= prices[-1]

    @allure.title("TC-E2E-09: Sort products by price (high to low)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_price_high_to_low(self, page):
        with allure.step("Select Price (high to low) sort option"):
            self.inventory_page.select_sort("hilo")

        with allure.step("Verify prices are strictly descending"):
            prices = self.inventory_page.get_item_prices()
            assert prices == sorted(prices, reverse=True)
            assert prices[0] >= prices[-1]

    @allure.title("TC-E2E-10: Sort products by name (Z to A)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_name_za(self, page):
        with allure.step("Select Name (Z to A) sort option"):
            self.inventory_page.select_sort("za")

        with allure.step("Verify names are reverse alphabetically sorted"):
            names = self.inventory_page.get_item_names()
            assert names == sorted(names, reverse=True)

    @allure.title("TC-E2E-11: Item detail page navigation, description inspection, and add to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_product_detail_page_and_cart(self, page):
        detail_page = ItemDetailPage(page)
        target_item = "Sauce Labs Backpack"

        with allure.step("Click on product title to open detail page"):
            self.inventory_page.click_item_title(target_item)

        with allure.step("Verify detail page contents"):
            assert "/inventory-item.html" in page.url
            assert detail_page.get_name() == target_item
            assert detail_page.get_price() == 29.99
            assert len(detail_page.get_description()) > 10

        with allure.step("Add to cart from detail page and navigate back"):
            detail_page.add_to_cart()
            assert self.inventory_page.get_cart_badge_count() == 1
            detail_page.back_to_products()
            assert "/inventory.html" in page.url
