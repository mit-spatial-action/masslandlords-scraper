#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import get
from csv import DictWriter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from time import sleep
from os import path

START_DATE = datetime.strptime("2020-10-24", "%Y-%m-%d")
URL = "https://masslandlords.net/policy/eviction-data"
WEEKLY = "/".join([URL, "filings-week-ending"])
MONTHLY = "/".join([URL, "filings-month"])
RESULTS = []
WEEKLY_CSV = "weekly-filings.csv"
MONTHLY_CSV = "weekly-filings.csv"


def create_date_list(start_date, end_date=False, freq="monthly"):
    """
    Create a list of week starts between a start and end date.
    """
    if freq == "monthly":
        delta = relativedelta(months=1)
        fmt = "%Y-%m"
    elif freq == "weekly":
        delta = relativedelta(days=7)
        fmt = "%Y-%m-%d"
        end_date = datetime.strptime("2023-07-01", "%Y-%m-%d")
    else:
        raise SystemExit(f"Error: {freq} is not a valid frequency.")
    if not end_date:
        end_date = datetime.today()
    date_list = []
    while start_date <= end_date:
        date_list.append(start_date.strftime(fmt))
        start_date += delta
    return date_list


def parse_page(page_request):
    """
    Parses requested page.
    """
    results = {"central": 0, "eastern": 0, "metro_south": 0, "northeast": 0, "southeast": 0, "western": 0}
    page = page_request.text.split()
    for i in range(len(page) - 1):
        if (page[i - 1][-1] == "%" or page[i - 1] == "Percent") & page[i + 1].isdigit():
            if page[i] in results.keys():
                results[page[i]] = page[i + 1]
            else:
                continue
        else:
            continue
    print(results)
    return results


def main():
    for date in create_date_list(START_DATE, freq="weekly"):
        request = get(f"{WEEKLY}-{date}")
        print(f"Attempting to download {date}.")
        if request.status_code == 404:
            print(f"😞 No data available for {date}. 😞")
            continue
        else:
            results = parse_page(request)
            results["date"] = date
            RESULTS.append(results)
        # Be courteous.
        sleep(1.5)

    with open(WEEKLY_CSV, "w") as csvfile:
        # creating a csv writer object
        writer = DictWriter(
            csvfile, fieldnames=["date", "central", "eastern", "metro_south", "northeast", "southeast", "western"]
        )
        # Write the header.
        writer.writeheader()
        # writing the data rows
        writer.writerows(RESULTS)
