"""
Base Page Object for Playwright with resilient waiting and interaction methods.
"""
from playwright.sync_api import Page, expect
from config.settings import settings


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = settings.BASE_URL

    def open(self, path: str = ""):
        target_url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(target_url, timeout=settings.DEFAULT_TIMEOUT)
        return self

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def wait_for_url_contains(self, fragment: str, timeout: int = settings.DEFAULT_TIMEOUT):
        self.page.wait_for_url(f"**/*{fragment}*", timeout=timeout)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        try:
            return self.page.locator(selector).is_visible(timeout=timeout)
        except Exception:
            return False

    def get_text(self, selector: str) -> str:
        return (self.page.locator(selector).first.text_content() or "").strip()

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.page.locator(selector).fill(text)

    def take_screenshot(self, name: str) -> bytes:
        return self.page.screenshot(path=f"reports/{name}.png", full_page=True)
