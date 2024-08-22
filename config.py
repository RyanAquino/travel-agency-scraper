from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
import os


proxies = [
    os.getenv("proxy-1"),
    os.getenv("proxy-2"),
]


# def get_driver_with_proxy(proxy):
#     chrome_options = ChromeOptions()
#     chrome_options.add_argument(f'--proxy-server={proxy}')
#     driver = webdriver.Chrome(options=chrome_options)
#
#     return driver


def chrome_settings_init():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(f'--proxy-server={proxies[0]}')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1900,1080")
    chrome_settings = {"options": chrome_options}

    return chrome_settings
