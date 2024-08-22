"""
Configuration related functions
"""

import os

from selenium.webdriver.chrome.options import Options as ChromeOptions


class Config:
    """Configurations."""

    # Hard coded for now - refactor to load values from .env
    PROXIES = [
        os.getenv("proxy-1"),
        os.getenv("proxy-2"),
    ]
    DRIVER_TIMEOUT = 10
    BASE_URL = "https://www.jalan.net/en/japan_hotels_ryokan/"


def chrome_settings_init() -> dict:
    """
    Create initial Chrome browser settings.

    :return: dictionary of Chrome browser settings
    """
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1900,1080")
    chrome_settings = {"options": chrome_options}

    return chrome_settings
