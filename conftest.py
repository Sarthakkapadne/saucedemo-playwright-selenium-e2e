"""
Pytest configuration for Playwright and Selenium test suites.
Includes cross-browser fixtures, failure screenshot attachments to Allure & HTML reports.
"""
import os
import pytest
import allure
from playwright.sync_api import sync_playwright, Browser, Page
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config.settings import settings


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        help="Browser for Playwright: chromium, firefox, webkit",
    )
    parser.addoption(
        "--headless-mode",
        action="store",
        default="true",
        help="Run browser in headless mode: true or false",
    )


@pytest.fixture(scope="session")
def is_headless(request) -> bool:
    val = request.config.getoption("--headless-mode")
    return val.lower() in ("true", "1", "yes")


# ==============================================================================
# Playwright Fixtures
# ==============================================================================
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance, request, is_headless) -> Browser:
    browser_type_name = request.config.getoption("--browser-name")
    browser_type = getattr(playwright_instance, browser_type_name, playwright_instance.chromium)
    browser = browser_type.launch(headless=is_headless)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser, request) -> Page:
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir="reports/videos/" if os.getenv("RECORD_VIDEO") else None,
    )
    page = context.new_page()
    yield page
    context.close()


# ==============================================================================
# Selenium WebDriver Fixtures
# ==============================================================================
@pytest.fixture(scope="function")
def selenium_driver(is_headless):
    options = ChromeOptions()
    if is_headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    yield driver
    driver.quit()


# ==============================================================================
# Screenshot on Failure Hook (Allure + Pytest-HTML)
# ==============================================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        screenshot_name = f"{item.name}_{report.when}.png"
        screenshot_path = os.path.join("reports/screenshots", screenshot_name)
        
        # Playwright Page screenshot
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                screenshot_bytes = page.screenshot(path=screenshot_path, full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name=f"Failure Screenshot: {item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                print(f"Failed to capture Playwright screenshot: {e}")
                
        # Selenium WebDriver screenshot
        elif "selenium_driver" in item.funcargs:
            driver = item.funcargs["selenium_driver"]
            try:
                driver.save_screenshot(screenshot_path)
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"Selenium Failure Screenshot: {item.name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
            except Exception as e:
                print(f"Failed to capture Selenium screenshot: {e}")
