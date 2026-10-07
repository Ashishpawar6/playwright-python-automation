import pytest

from config import settings


@pytest.mark.smoke
def test_valid_user_can_log_in(login_page, inventory_page):
    login_page.open()
    login_page.login(settings.STANDARD_USER, settings.PASSWORD)

    inventory_page.expect_url_contains("/inventory.html")
    inventory_page.expect_text(inventory_page.title, "Products")
    assert inventory_page.count_of(inventory_page.items) == 6


@pytest.mark.regression
def test_locked_out_user_sees_error(login_page):
    login_page.open()
    login_page.login(settings.LOCKED_OUT_USER, settings.PASSWORD)

    login_page.expect_visible(login_page.error_message)
    assert "locked out" in login_page.error_text()


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        (settings.STANDARD_USER, "wrong_password", "Username and password do not match"),
        ("no_such_user", settings.PASSWORD, "Username and password do not match"),
        ("", settings.PASSWORD, "Username is required"),
        (settings.STANDARD_USER, "", "Password is required"),
    ],
    ids=["wrong-password", "unknown-user", "missing-username", "missing-password"],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    login_page.open()
    login_page.login(username, password)

    login_page.expect_contains_text(login_page.error_message, expected_error)
    login_page.expect_url_contains("saucedemo.com")
    assert "inventory" not in login_page.current_url()
