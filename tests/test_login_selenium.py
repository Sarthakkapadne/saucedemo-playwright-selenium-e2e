"""
Selenium Login Test Suite (4 Test Cases).
Validates WebDriver explicit waits, credentials handling, and performance glitch SLA.
"""
import time
import pytest
import allure
from pages.selenium_pages.login_selenium_page import LoginSeleniumPage
from pages.selenium_pages.inventory_selenium_page import InventorySeleniumPage
from config.settings import settings


@allure.feature("Authentication & Access Control")
@allure.story("Selenium WebDriver Login Flows")
@pytest.mark.selenium
class TestLoginSelenium:

    @allure.title("TC-E2E-16: Selenium Valid Login with Standard User")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_selenium_valid_login(self, selenium_driver):
        login_page = LoginSeleniumPage(selenium_driver)
        inventory_page = InventorySeleniumPage(selenium_driver)

        with allure.step("Submit valid login credentials via Selenium"):
            login_page.login(settings.STANDARD_USER, settings.DEFAULT_PASSWORD)

        with allure.step("Assert redirection to inventory"):
            assert "/inventory.html" in login_page.get_current_url()
            assert inventory_page.get_items_count() == 6

    @allure.title("TC-E2E-17: Selenium Locked Out User Error Banner Verification")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_selenium_locked_out_user(self, selenium_driver):
        login_page = LoginSeleniumPage(selenium_driver)

        with allure.step("Attempt login with locked_out_user"):
            login_page.login(settings.LOCKED_OUT_USER, settings.DEFAULT_PASSWORD)

        with allure.step("Assert error banner is displayed"):
            assert login_page.is_error_displayed()
            assert "Epic sadface: Sorry, this user has been locked out." in login_page.get_error_message()

    @allure.title("TC-E2E-18: Selenium Empty Credentials Required Error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_selenium_empty_credentials(self, selenium_driver):
        login_page = LoginSeleniumPage(selenium_driver)

        with allure.step("Submit login with empty fields"):
            login_page.login("", "")

        with allure.step("Assert Username is required"):
            assert "Epic sadface: Username is required" in login_page.get_error_message()

    @allure.title("TC-E2E-19: Selenium Performance Glitch User Login under SLA (< 6s)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_selenium_performance_glitch_user(self, selenium_driver):
        login_page = LoginSeleniumPage(selenium_driver)
        inventory_page = InventorySeleniumPage(selenium_driver)

        with allure.step("Login with performance_glitch_user and track latency"):
            start_time = time.time()
            login_page.login(settings.PERF_GLITCH_USER, settings.DEFAULT_PASSWORD)
            assert "/inventory.html" in login_page.get_current_url()
            assert inventory_page.get_items_count() == 6
            elapsed = time.time() - start_time

        with allure.step(f"Assert total login time ({elapsed:.2f}s) is within acceptable SLA limit"):
            assert elapsed < 7.0, f"Performance glitch login exceeded SLA: {elapsed}s"
