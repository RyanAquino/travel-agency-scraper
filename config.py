"""
Configuration related functions
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver


class Config:
    """Configurations."""

    # Hard coded for now - refactor to load values from .env and add validation
    PROXIES = [
        os.getenv("proxy-1"),
        os.getenv("proxy-2"),
    ]
    DRIVER_TIMEOUT = 30
    BASE_URL = "https://www.jalan.net/en/japan_hotels_ryokan/"
    proxy_idx = 0

    @staticmethod
    def generate_base_settings() -> ChromeOptions:
        """
        Generate chrome base settings.

        :return: chrome base settings
        """
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1900,1080")

        return chrome_options

    @classmethod
    def get_current_proxy(cls) -> str:
        """
        Get current proxy in a round-robin fashion.

        :return: proxy
        """
        proxy = cls.PROXIES[cls.proxy_idx]
        cls.proxy_idx = (cls.proxy_idx + 1) % len(cls.PROXIES)

        return proxy

    @classmethod
    def create_driver_with_proxy(cls) -> WebDriver:
        """
        Create driver with the chosen proxy.
        :return: selenium chrome driver
        """
        proxy = cls.get_current_proxy()
        chrome_options = Config.generate_base_settings()
        chrome_options.add_argument(f"--proxy-server={proxy}")

        return webdriver.Chrome(options=chrome_options)
