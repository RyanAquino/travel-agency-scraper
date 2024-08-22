"""
Crawler functions.
"""

import re

from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from action_utils import find_element_by_xpath, find_visible_elements_by_xpath
from config import Config


class Crawler:
    """
    Main crawler class that contains functions related to scraping the site.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize class dependencies.

        :param driver: chrome driver
        """
        self.driver = driver

    def perform_search(self, search_prefecture: str):
        """
        Perform prefecture search and submit the form to page.

        :param search_prefecture: search input prefecture
        :return: None
        """
        inputs = Select(
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//select[@name='quickSearchDestination' and @id='quickSearchDestination']",
                    )
                )
            )
        )

        for idx, item in enumerate(inputs.options):
            if item.text == search_prefecture:
                inputs.select_by_index(idx)
                break

        submit_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@id='jsi-submit-btn']"))
        )
        self.driver.execute_script("arguments[0].click();", submit_element)

    def scrape_search_data(self) -> dict:
        """
        Scrape search date params set.

        :return: tuple of checkin and checkout dates
        """
        checkin_in_element = find_element_by_xpath(
            self.driver, "//input[@name='checkinDate']"
        )
        checkin_out_element = find_element_by_xpath(
            self.driver, "//input[@name='checkoutDate']"
        )

        room_count_element = find_element_by_xpath(
            self.driver, "//input[@name='roomCount']"
        )
        adult_num_element = find_element_by_xpath(
            self.driver, "//input[@name='adultNum']"
        )

        checkin_dt = checkin_in_element.get_attribute("value")
        checkout_dt = checkin_out_element.get_attribute("value")
        room_count = room_count_element.get_attribute("value")
        adult_num = adult_num_element.get_attribute("value")

        return {
            "checkin": checkin_dt,
            "checkout": checkout_dt,
            "room_count": room_count,
            "adult_num": adult_num,
        }

    @staticmethod
    def scrape_room_type_sub_rooms(room_plan_name: str, sub_rooms: list):
        sub_room_types = []

        for sub_room in sub_rooms:
            prices_option = sub_room.find("div", class_="plan-item-price")
            yen_price = prices_option.find("p", class_="jpy").text
            usd_price = prices_option.find("p", class_="usd").text
            yen_price = int("".join(re.findall(r"\d+", yen_price)))
            usd_price = int("".join(re.findall(r"\d+", usd_price)))

            sub_room_types.append(
                {
                    "type": room_plan_name,
                    "jp_price": yen_price,
                    "us_price": usd_price,
                }
            )

        return sub_room_types

    def scrape_room_types(self, room_types: list) -> list[dict]:
        """
        Scrape different room types of a hotel.

        :param room_types: list of room types
        :return: list of room type data containing keys (type, jp_price, us_price)
        """
        room_type_data = []

        for room in room_types:
            room_plan_soup = room.find("div", class_="room-plan cf")
            room_plan_name = room_plan_soup.find("div", class_="room-plan-text").h4.text

            room_details_soup = room.find("div", class_="plan-item").ul
            sub_rooms = room_details_soup.findAll("li", recursive=False)
            room_type_data += self.scrape_room_type_sub_rooms(room_plan_name, sub_rooms)

        return room_type_data

    def scrape_hotel_details(self, hotel_url) -> dict:
        """
        Scrape single hotel page.

        :param hotel_url: hotel url to be scraped
        :return: dictionary of hotel details containing (hotel name, location, room types, pricing options in USD and YEN)
        """
        with Config.create_driver_with_proxy() as proxy_driver:
            proxy_driver.get(hotel_url)
            html_source = proxy_driver.page_source
            soup = BeautifulSoup(html_source, "html.parser")

            hotel_name_container = soup.find("div", class_="hotel-name-container")
            hotel_name = hotel_name_container.find_all("h1")[-1].text
            location = soup.find("address", class_="hotel-address").text

            room_list = soup.find("div", class_="room-list-container")
            room_types = room_list.findAll("div", class_="room-plan-list")
            room_types_data = self.scrape_room_types(room_types)

            return {
                "name": hotel_name,
                "location": location,
                "room_types": room_types_data,
            }

    def scrape_hotel_urls(self) -> list[str]:
        """
        Scrape hotel URLs of the current page.

        :return: list of hotel URLs
        """
        hotels_links = find_visible_elements_by_xpath(
            self.driver,
            "//ul[@id='jsi-cassette-container']/li//h3[@class='cassette-hotel-name']//a",
        )
        hotel_urls = []

        for hotel in hotels_links:
            hotel_url = hotel.get_attribute("href")
            hotel_urls.append(hotel_url)

        return hotel_urls

    def scrape_hotels(self) -> list[dict]:
        """
        Scrape hotel details (Name, location, Room Types, prices with pricing options) up until last available page.

        :return: list of hotel details containing (name, location, list of room_types)
        """
        hotel_details = []
        prev_url = self.driver.current_url
        next_page = find_element_by_xpath(self.driver, "//li[@class='next']")

        while next_page:
            hotel_urls = self.scrape_hotel_urls()

            for hotel_url in hotel_urls:
                hotel_detail = self.scrape_hotel_details(hotel_url)
                hotel_details.append(hotel_detail)
                logger.info(f"Data: {hotel_detail}")

            self.driver.get(prev_url)
            next_page = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='next']"))
            )
            self.driver.execute_script("arguments[0].click();", next_page)

            if len(hotel_urls) < 30 or prev_url == self.driver.current_url:
                break

            prev_url = self.driver.current_url

        return hotel_details
