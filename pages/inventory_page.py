from pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.title = self.by_test_id("title")
        self.items = self.by_test_id("inventory-item")
        self.item_names = self.by_test_id("inventory-item-name")
        self.item_prices = self.by_test_id("inventory-item-price")
        self.sort_dropdown = self.by_test_id("product-sort-container")
        self.cart_link = self.by_test_id("shopping-cart-link")
        self.cart_badge = self.by_test_id("shopping-cart-badge")

    def add_to_cart(self, product: str) -> None:
        self.click(self.by_test_id(f"add-to-cart-{product}"))

    def remove_from_cart(self, product: str) -> None:
        self.click(self.by_test_id(f"remove-{product}"))

    def sort_by(self, option: str) -> None:
        """option: az, za, lohi or hilo"""
        self.select_option(self.sort_dropdown, option)

    def product_names(self) -> list[str]:
        return self.texts_of(self.item_names)

    def product_prices(self) -> list[float]:
        return [float(p.lstrip("$")) for p in self.texts_of(self.item_prices)]

    def open_cart(self) -> None:
        self.click(self.cart_link)
