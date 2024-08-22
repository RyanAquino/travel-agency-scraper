"""
Reporting functions.
"""

import csv

from loguru import logger


def generate_csv_report(
    search_data: dict,
    hotel_details: list[dict],
):
    """
    Generate CSV summary report based on the search terms and hotel results.

    :param search_data: Search data filters
    :param hotel_details: list of hotel details
    :return: None
    """
    search_prefecture = search_data.get("prefecture")
    checkin_dt = search_data.get("checkin")
    checkout_dt = search_data.get("checkout")
    room_count = search_data.get("room_count")
    adult_num = search_data.get("adult_num")

    filename = f"./results/{search_prefecture}_hotels.csv"
    with open(filename, mode="w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Summary"])
        writer.writerow(["Prefecture", search_prefecture])
        writer.writerow(["From date", checkin_dt])
        writer.writerow(["To date", checkout_dt])
        writer.writerow(["Room Count", room_count])
        writer.writerow(["Number of Adults", adult_num])
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
    logger.success(f"Done generating CSV report: {filename}")
