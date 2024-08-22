import csv
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from config import chrome_settings_init


def scrape_item_details(driver, hotel_url):
    driver.get(hotel_url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")

    hotel_name_container = soup.find("div", class_="hotel-name-container")
    hotel_name = hotel_name_container.find_all("h1")[-1].text
    location = soup.find("address", class_="hotel-address").text

    room_list = soup.find("div", class_="room-list-container")
    room_types = room_list.findAll("div", class_="room-plan-list")

    room_type_data = []

    for room in room_types:
        room_plan_soup = room.find("div", class_="room-plan cf")
        room_plan_name = room_plan_soup.find("div", class_="room-plan-text").h4.text

        room_details_soup = room.find("div", class_="plan-item").ul
        sub_rooms = room_details_soup.findAll("li", recursive=False)

        for sub_room in sub_rooms:
            prices_option = sub_room.find("div", class_="plan-item-price")
            yen_price = prices_option.find("p", class_="jpy").text
            usd_price = prices_option.find("p", class_="usd").text
            yen_price = int("".join(re.findall(r"\d+", yen_price)))
            usd_price = int("".join(re.findall(r"\d+", usd_price)))

            room_type_data.append(
                {
                    "type": room_plan_name,
                    "jp_price": yen_price,
                    "us_price": usd_price,
                }
            )

    return {
        "name": hotel_name,
        "location": location,
        "room_types": room_type_data,
    }


def main():
    search_prefecture = "Tokyo"
    base_url = "https://www.jalan.net/en/japan_hotels_ryokan/"

    chrome_config = chrome_settings_init()

    with webdriver.Chrome(**chrome_config) as driver:
        driver.get(base_url)

        inputs = Select(
            WebDriverWait(driver, 10).until(
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

        checkin_in_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='checkinDate']"))
        )
        checkin_out_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='checkoutDate']"))
        )
        checkin_dt = checkin_in_element.get_attribute("value")
        checkout_dt = checkin_out_element.get_attribute("value")

        submit_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@id='jsi-submit-btn']"))
        )
        driver.execute_script("arguments[0].click();", submit_element)

        hotel_details = []

        prev_url = driver.current_url
        next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@class='next']"))
        )

        # while next_page:

        hotels_links = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    "//ul[@id='jsi-cassette-container']/li//h3[@class='cassette-hotel-name']//a",
                )
            )
        )
        hotel_urls = []

        for hotel in hotels_links:
            hotel_url = hotel.get_attribute("href")
            hotel_urls.append(hotel_url)

        for hotel_url in hotel_urls:
            hotel_detail = scrape_item_details(driver, hotel_url)
            hotel_details.append(hotel_detail)
            print(hotel_detail)
            break

            # driver.get(prev_url)
            # next_page = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//li[@class='next']"))
            # )
            # driver.execute_script("arguments[0].click();", next_page)
            #
            # if len(hotels_links) < 30 or prev_url == driver.current_url:
            #     break
            #
            # prev_url = driver.current_url

    with open(f"{search_prefecture}_hotels.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Summary"])
        writer.writerow(["Prefecture", search_prefecture])
        writer.writerow(["From date", checkin_dt])
        writer.writerow(["To date", checkout_dt])
        writer.writerow(["Total hotels count", len(hotel_details)])

        writer.writerow([])

        writer.writerow(["Hotel List Details"])
        writer.writerow(["Name", "Location", "Room Type", "JPY Price", "US Price"])

        for hotel in hotel_details:
            for room in hotel["room_types"]:
                writer.writerow(
                    [
                        hotel["name"],
                        hotel["location"],
                        room["type"],
                        room["jp_price"],
                        room["us_price"],
                    ]
                )


if __name__ == "__main__":
    main()
