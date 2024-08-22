from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import Config


def find_element_by_xpath(driver, xpath):
    return WebDriverWait(driver, Config.DRIVER_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def find_visible_elements_by_xpath(driver, xpath):
    return WebDriverWait(driver, Config.DRIVER_TIMEOUT).until(
        EC.visibility_of_all_elements_located(
            (
                By.XPATH,
                xpath,
            )
        )
    )
