from pages.common_methods import CommonMethods
from pages.locators import *


class LoginPage(CommonMethods):

    def __init__(self, browser):
        super().__init__(browser)

    def login(self):
        self.navigate(self.config.get("base_url"))
        self.click(login_link)
        self.input(username, self.config.get("username"))
        self.input(password, self.config.get("password"))
        self.click(login_btn)
        self.take_screenshot()

    def logout(self):
        self.navigate(self.config.get("base_url"))
        self.click(logout_link)
        self.take_screenshot()
