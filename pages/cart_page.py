from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.items = self.by_test_id("inventory-item")
        self.item_names = self.by_test_id("inventory-item-name")
        self.checkout_button = self.by_test_id("checkout")
        self.continue_shopping_button = self.by_test_id("continue-shopping")

    def product_names(self) -> list[str]:
        return self.texts_of(self.item_names)

    def remove(self, product: str) -> None:
        self.click(self.by_test_id(f"remove-{product}"))

    def checkout(self) -> None:
        self.click(self.checkout_button)
