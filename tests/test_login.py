import pytest

from conftest import allure_step
from pages.login import LoginPage


@pytest.mark.a
@allure_step("Login")
def test_one(browser):
    login_page = LoginPage(browser)
    login_page.login()


@pytest.mark.b
@allure_step("Logout")
def test_two(browser):
    login_page = LoginPage(browser)
    login_page.logout()
