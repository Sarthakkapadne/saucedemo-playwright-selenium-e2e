"""
Base Page Object for Selenium WebDriver with explicit WebDriverWait.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from config.settings import settings


class BaseSeleniumPage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.base_url = settings.BASE_URL

    def open(self, path: str = ""):
        target = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        self.driver.get(target)
        return self

    def find(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def find_all(self, by, locator):
        try:
            self.wait.until(EC.presence_of_element_located((by, locator)))
            return self.driver.find_elements(by, locator)
        except TimeoutException:
            return []

    def click(self, by, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
            element.click()
        except StaleElementReferenceException:
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
            element.click()

    def type_text(self, by, locator, text: str):
        element = self.find(by, locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, locator) -> str:
        return self.find(by, locator).text.strip()

    def is_visible(self, by, locator, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title
