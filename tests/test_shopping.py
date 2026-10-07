import pytest

from config import settings


@pytest.mark.smoke
def test_adding_items_updates_cart_badge(logged_in):
    logged_in.add_to_cart(settings.BACKPACK)
    logged_in.expect_text(logged_in.cart_badge, "1")

    logged_in.add_to_cart(settings.BIKE_LIGHT)
    logged_in.expect_text(logged_in.cart_badge, "2")


@pytest.mark.regression
def test_removing_item_clears_cart_badge(logged_in):
    logged_in.add_to_cart(settings.BACKPACK)
    logged_in.remove_from_cart(settings.BACKPACK)

    logged_in.expect_hidden(logged_in.cart_badge)


@pytest.mark.regression
def test_cart_lists_the_items_that_were_added(logged_in, cart_page):
    logged_in.add_to_cart(settings.BACKPACK)
    logged_in.add_to_cart(settings.BIKE_LIGHT)
    logged_in.open_cart()

    cart_page.expect_url_contains("/cart.html")
    assert sorted(cart_page.product_names()) == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@pytest.mark.regression
@pytest.mark.parametrize(
    "option, key, reverse",
    [("az", str.lower, False), ("za", str.lower, True)],
    ids=["name-a-to-z", "name-z-to-a"],
)
def test_sort_products_by_name(logged_in, option, key, reverse):
    logged_in.sort_by(option)

    names = logged_in.product_names()
    assert names == sorted(names, key=key, reverse=reverse)


@pytest.mark.regression
@pytest.mark.parametrize("option, reverse", [("lohi", False), ("hilo", True)], ids=["low-to-high", "high-to-low"])
def test_sort_products_by_price(logged_in, option, reverse):
    logged_in.sort_by(option)

    prices = logged_in.product_prices()
    assert prices == sorted(prices, reverse=reverse)


@pytest.mark.smoke
def test_complete_checkout_end_to_end(logged_in, cart_page, checkout_page):
    logged_in.add_to_cart(settings.BACKPACK)
    logged_in.open_cart()
    cart_page.checkout()

    checkout_page.fill_information("Asha", "Rao", "560001")
    checkout_page.continue_to_overview()
    checkout_page.expect_url_contains("/checkout-step-two.html")
    checkout_page.expect_contains_text(checkout_page.summary_total, "Total: $")

    checkout_page.finish()
    checkout_page.expect_text(checkout_page.complete_header, "Thank you for your order!")


@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Rao", "560001", "First Name is required"),
        ("Asha", "", "560001", "Last Name is required"),
        ("Asha", "Rao", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_requires_all_information(logged_in, cart_page, checkout_page, first, last, postal, expected_error):
    logged_in.add_to_cart(settings.BACKPACK)
    logged_in.open_cart()
    cart_page.checkout()

    checkout_page.fill_information(first, last, postal)
    checkout_page.continue_to_overview()

    checkout_page.expect_contains_text(checkout_page.error_message, expected_error)
    checkout_page.expect_url_contains("/checkout-step-one.html")
