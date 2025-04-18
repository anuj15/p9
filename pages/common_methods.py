import os
from datetime import datetime as dt
from pathlib import Path

import allure
import pytest

from utils.config_manager import ConfigManager
from utils.log_manager import LogManager


class CommonMethods:

    def __init__(self, browser):
        self.browser = browser
        self.log = LogManager().get_logger()
        self.config = ConfigManager()

    def navigate(self, url):
        self.browser.goto(url)
        self.log.info(f"Navigated to: {url}")

    def click(self, selector):
        self.browser.locator(selector).click()
        self.log.info(f"Clicked on: {selector}")

    def input(self, selector, value):
        self.browser.locator(selector).fill(value)
        self.log.info(f"Input '{value}' into: {selector}")

    def take_screenshot(self):
        file_path = Path(__file__).resolve().parents[1] / self.config.get("screenshots_path")
        file_path = os.path.join(file_path, dt.strftime(dt.now(), "%Y_%m_%d_%H_%M_%S") + ".png")
        self.browser.screenshot(path=file_path)
        allure.attach.file(file_path, attachment_type=allure.attachment_type.PNG)
        pytest.extra_screenshot = file_path
        self.log.info("Screenshot captured successfully")
        return file_path
