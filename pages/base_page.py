"""Common actions shared by every page object.

Page objects hold *what* is on a page (locators) and *what a user can do* there.
This base class holds the generic *how* (click, type, read, wait, assert helpers),
so those details live in exactly one place.
"""
import re

from playwright.sync_api import Locator, Page, expect

from config import settings


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    # --- navigation ---------------------------------------------------------------------
    def open(self) -> None:
        self.page.goto(f"{settings.BASE_URL}{self.path}")

    def current_url(self) -> str:
        return self.page.url

    # --- element actions ----------------------------------------------------------------
    def by_test_id(self, test_id: str) -> Locator:
        """The sample site marks elements with data-test attributes (see conftest)."""
        return self.page.get_by_test_id(test_id)

    def click(self, locator: Locator) -> None:
        locator.click()

    def type_into(self, locator: Locator, text: str) -> None:
        locator.fill(text)

    def select_option(self, locator: Locator, value: str) -> None:
        locator.select_option(value)

    def text_of(self, locator: Locator) -> str:
        return locator.inner_text().strip()

    def texts_of(self, locator: Locator) -> list[str]:
        return [t.strip() for t in locator.all_inner_texts()]

    def count_of(self, locator: Locator) -> int:
        return locator.count()

    # --- waits and assertions (Playwright's web-first assertions retry automatically) -----
    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def expect_hidden(self, locator: Locator) -> None:
        expect(locator).to_be_hidden()

    def expect_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_have_text(text)

    def expect_contains_text(self, locator: Locator, text: str) -> None:
        expect(locator).to_contain_text(text)

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))
