"""
Main function.
"""

from selenium import webdriver

from config import Config, chrome_settings_init
from crawler import Crawler
from reporting import generate_csv_report


def main():
    """
    Main entrypoint of the program.
    :return: None
    """
    search_prefecture = "Tokyo"  # Hard coded for now including all default params (from date, to date, rooms)
    chrome_config = chrome_settings_init()

    with webdriver.Chrome(**chrome_config) as driver:
        driver.get(Config.BASE_URL)

        crawler = Crawler(driver)
        checkin_dt, checkout_dt = crawler.scrape_search_date_params()
        crawler.perform_search(search_prefecture)
        hotel_details = crawler.scrape_hotels()

    # Refactor to save row records on the fly
    generate_csv_report(search_prefecture, checkin_dt, checkout_dt, hotel_details)


if __name__ == "__main__":
    main()
