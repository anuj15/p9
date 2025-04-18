import base64
import functools
import os
import shutil
import subprocess
from pathlib import Path

import allure
import pytest
from playwright.sync_api import sync_playwright
from pytest_html import extras
from pytest_metadata.plugin import metadata_key

from utils.config_manager import ConfigManager
from utils.emailer import send_mail
from utils.env_manager import get_env
from utils.log_manager import LogManager

obj_config = ConfigManager()
logger = LogManager().get_logger()
root_dir = Path(__file__).resolve().parent
allure_result_path = root_dir / obj_config.get("allure_result_path")
allure_report_path = root_dir / obj_config.get("allure_report_path")


def pytest_configure(config):
    report_folder_path = root_dir / obj_config.get("report_folder_path")
    html_report_path = root_dir / obj_config.get("html_report_path")
    log_file_path = root_dir / obj_config.get("log_file_path")

    config.option.htmlpath = html_report_path
    config.option.self_contained_html = True
    config.option.allure_report_dir = allure_result_path
    config.option.strict_markers = True
    config.option.reruns = 1
    config.option.disable_warnings = True
    config.addinivalue_line("markers", "c")
    config.addinivalue_line("markers", "d")
    config.addinivalue_line("markers", "e")

    config.stash[metadata_key]["Project"] = obj_config.get("project_title")
    config.stash[metadata_key]["Environment"] = obj_config.get("environment")
    config.stash[metadata_key]["Browser"] = obj_config.get("browser")
    config.stash[metadata_key]["URL"] = obj_config.get("base_url")

    shutil.rmtree(report_folder_path, ignore_errors=True)
    os.makedirs(report_folder_path, exist_ok=True)
    os.makedirs(allure_report_path, exist_ok=True)
    os.makedirs(allure_result_path, exist_ok=True)

    with open(log_file_path, "w") as lf:
        lf.write("")


def pytest_html_report_title(report):
    report.title = obj_config.get("project_title")


@pytest.fixture(scope="session", autouse=True)
def browser():
    browser_name = obj_config.get("browser")
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=obj_config.get("headless"), args=["--start-maximized"])
        logger.info("Browser launched successfully")
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        context.close()
        browser.close()
        logger.info("Browser closed successfully")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.when == "call":
        screenshot = getattr(pytest, "extra_screenshot", None)
        if screenshot and os.path.exists(screenshot):
            if not hasattr(report, "extra"):
                report.extra = []
            with open(screenshot, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                html_img = f"<img src='data:image/png;base64, {encoded}' />"
                report.extra.append(extras.html(html_img))
            pytest.extra_screenshot = None


def allure_step(step_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with allure.step(step_name.format(*args, **kwargs)):
                return func(*args, **kwargs)

        return wrapper

    return decorator


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish():
    if get_env("LOCAL_EXECUTION"):
        os.chdir(root_dir)
        subprocess.run(["allure.bat", "generate", allure_result_path, "-o", allure_report_path, "--clean"])
        send_mail()
