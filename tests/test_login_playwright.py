"""
Playwright Login Test Suite (5 Test Cases).
Validates authentication flows, error banners, and edge cases.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import settings


@allure.feature("Authentication & Access Control")
@allure.story("Playwright Login Flows")
@pytest.mark.playwright
class TestLoginPlaywright:

    @allure.title("TC-E2E-01: Valid user login redirects to inventory")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_valid_login_standard_user(self, page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        with allure.step("Navigate to SauceDemo and submit valid credentials"):
            login_page.login(settings.STANDARD_USER, settings.DEFAULT_PASSWORD)

        with allure.step("Verify redirection to inventory catalog"):
            assert "/inventory.html" in page.url
            assert inventory_page.is_loaded()
            assert inventory_page.get_item_count() == 6

    @allure.title("TC-E2E-02: Locked out user displays appropriate error banner")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_locked_out_user(self, page):
        login_page = LoginPage(page)

        with allure.step("Attempt login with locked_out_user"):
            login_page.login(settings.LOCKED_OUT_USER, settings.DEFAULT_PASSWORD)

        with allure.step("Assert locked out error message"):
            assert login_page.is_error_displayed()
            error_text = login_page.get_error_message()
            assert "Epic sadface: Sorry, this user has been locked out." in error_text

    @allure.title("TC-E2E-03: Problem user logs in and loads catalog")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_problem_user(self, page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        with allure.step("Login with problem_user"):
            login_page.login(settings.PROBLEM_USER, settings.DEFAULT_PASSWORD)

        with allure.step("Assert catalog page loads"):
            assert "/inventory.html" in page.url
            assert inventory_page.get_item_count() == 6

    @allure.title("TC-E2E-04: Empty username validation shows required error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_username_validation(self, page):
        login_page = LoginPage(page)

        with allure.step("Attempt login with empty credentials"):
            login_page.login("", "")

        with allure.step("Assert Username is required error"):
            assert login_page.is_error_displayed()
            assert "Epic sadface: Username is required" in login_page.get_error_message()

    @allure.title("TC-E2E-05: Invalid password displays mismatch error")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_invalid_password_validation(self, page):
        login_page = LoginPage(page)

        with allure.step("Login with valid user but wrong password"):
            login_page.login(settings.STANDARD_USER, "wrong_password_999")

        with allure.step("Assert credentials mismatch error"):
            assert login_page.is_error_displayed()
            assert "Username and password do not match" in login_page.get_error_message()
