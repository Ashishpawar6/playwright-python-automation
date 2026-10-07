from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = self.by_test_id("error")

    def login(self, username: str, password: str) -> None:
        self.type_into(self.username_input, username)
        self.type_into(self.password_input, password)
        self.click(self.login_button)

    def error_text(self) -> str:
        return self.text_of(self.error_message)
