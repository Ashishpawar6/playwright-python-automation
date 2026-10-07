import pytest
from playwright.sync_api import Page

from config import settings
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}}


@pytest.fixture(autouse=True)
def configure_playwright(playwright):
    # The sample site identifies elements with data-test="...", not data-testid.
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def logged_in(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """Start a test already signed in as the standard user, on the products page."""
    login_page.open()
    login_page.login(settings.STANDARD_USER, settings.PASSWORD)
    inventory_page.expect_url_contains("/inventory.html")
    return inventory_page
