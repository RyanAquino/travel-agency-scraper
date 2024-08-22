"""
Reporting functions.
"""

import csv

from loguru import logger


def generate_csv_report(
    search_prefecture: str,
    checkin_dt: str,
    checkout_dt: str,
    hotel_details: list[dict],
):
    """
    Generate CSV summary report based on the search terms and hotel results.

    :param search_prefecture: Search prefecture name
    :param checkin_dt: checkin date
    :param checkout_dt: checkout date
    :param hotel_details: list of hotel details
    :return: None
    """
    filename = f"{search_prefecture}_hotels.csv"
    with open(filename, mode="w", newline="") as file:
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
    logger.success(f"Done generating CSV report: {filename}")
