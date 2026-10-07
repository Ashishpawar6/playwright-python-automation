from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Covers the three checkout steps: your information, overview, and completion."""

    def __init__(self, page):
        super().__init__(page)
        self.first_name = self.by_test_id("firstName")
        self.last_name = self.by_test_id("lastName")
        self.postal_code = self.by_test_id("postalCode")
        self.continue_button = self.by_test_id("continue")
        self.finish_button = self.by_test_id("finish")
        self.error_message = self.by_test_id("error")
        self.summary_total = self.by_test_id("total-label")
        self.complete_header = self.by_test_id("complete-header")

    def fill_information(self, first: str, last: str, postal: str) -> None:
        self.type_into(self.first_name, first)
        self.type_into(self.last_name, last)
        self.type_into(self.postal_code, postal)

    def continue_to_overview(self) -> None:
        self.click(self.continue_button)

    def finish(self) -> None:
        self.click(self.finish_button)

    def error_text(self) -> str:
        return self.text_of(self.error_message)
