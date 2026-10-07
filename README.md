# Playwright + Python Test Automation

An end-to-end UI test framework using **Playwright**, **pytest** and the **Page Object Model**. It tests the public demo shop [saucedemo.com](https://www.saucedemo.com): login, product browsing and sorting, the cart, and checkout.

## Structure

```
pages/
  base_page.py        Common methods shared by every page (click, type, read text, waits/assertions)
  login_page.py       Locators + actions for the login page
  inventory_page.py   Locators + actions for the products page
  cart_page.py        Locators + actions for the cart
  checkout_page.py    Locators + actions for the checkout steps
tests/
  conftest.py         Fixtures: page objects and a ready-logged-in state
  test_login.py       Login scenarios (valid, locked out, 4 invalid-input cases)
  test_shopping.py    Cart, sorting and checkout scenarios
config/settings.py    Base URL, demo credentials and product names (test data)
pytest.ini            Markers and default options
```

**Design rules**

- **Locators live only in page objects.** Tests never contain a selector, so a UI change is fixed in one place.
- **Common methods live in one file**, `pages/base_page.py`, which every page object inherits from.
- **Tests read like user stories** (`login`, `add_to_cart`, `checkout`) and contain the assertions; page objects contain no test logic beyond waiting for their own elements.
- **Stable locators:** the site's `data-test` attributes are used instead of brittle CSS/XPath (`set_test_id_attribute` in `conftest.py`).
- **No sleeps.** Playwright auto-waits, and the assertions (`expect(...)`) retry until they pass or time out.
- **Data-driven tests** use `pytest.mark.parametrize`, so the four invalid-login cases and the three checkout-validation cases are each one test function.
- **Markers:** `smoke` for the critical path, `regression` for broader coverage.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
pytest                      # all tests, headless
pytest -m smoke             # only the smoke tests
pytest --headed --slowmo 500   # watch the browser
pytest tests/test_login.py  # a single file
pytest -k checkout          # tests whose name contains "checkout"
BASE_URL=https://www.saucedemo.com pytest   # point at another environment
```

On failure, a screenshot and a Playwright trace are kept under `test-results/`. Open a trace with:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

## Test coverage

| Area | Scenarios |
|---|---|
| Login | valid login, locked-out user, wrong password, unknown user, missing username, missing password |
| Cart | add items updates the badge, remove clears it, cart lists the added items |
| Sorting | name A–Z / Z–A, price low–high / high–low |
| Checkout | full purchase end to end, missing first name / last name / postal code |

## Notes

- The tests depend on a third-party demo site, so they need internet access, and a change on that site can break them.
- Each test starts from a fresh browser context (pytest-playwright default), so tests are independent and can run in any order.
