#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import Session, RequestException
from csv import DictWriter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from time import sleep
from os import path

START_DATE = datetime.strptime("2020-10-24", "%Y-%m-%d")
MONTHLY_START_DATE = datetime.strptime("2020-11-01", "%Y-%m-%d")
WEEKLY_END_DATE = datetime.strptime("2023-07-01", "%Y-%m-%d")
URL = "https://masslandlords.net/policy/eviction-data"
WEEKLY_URL = "/".join([URL, "filings-week-ending"])
MONTHLY_URL = "/".join([URL, "filings-month"])
WEEKLY_CSV = "weekly-filings.csv"
MONTHLY_CSV = "monthly-filings.csv"
COURTS = ["central", "eastern", "metro_south", "northeast", "southeast", "western"]


def create_date_list(start_date, end_date=False, freq="monthly"):
    """
    Create a list of week starts between a start and end date.
    """
    if freq == "monthly":
        delta = relativedelta(months=1)
    elif freq == "weekly":
        delta = relativedelta(days=7)
    else:
        raise SystemExit(f"Error: {freq} is not a valid frequency.")
    if not end_date:
        end_date = datetime.today()
    date_list = []
    while start_date <= end_date:
        last_day_of_month = start_date + relativedelta(months=1) - relativedelta(days=1)
        date_list.append(last_day_of_month.strftime("%Y-%m-%d"))
        start_date += delta
    return date_list


def parse_page(page_request):
    """
    Parses requested page.
    """
    results = dict.fromkeys(COURTS, 0)
    page = page_request.text.split()
    for i in range(len(page) - 1):
        if (page[i - 1][-1] == "%" or page[i - 1] == "Percent") & page[i + 1].isdigit():
            if page[i] in results.keys():
                results[page[i]] = page[i + 1]
            else:
                continue
        else:
            continue
    return results

def scrape_date_list(date_list, base_url, out_csv):
    results = []

    with Session() as session:
        for d in date_list:
            url = f"{base_url}-{d}"
            print(f"Attempting to download {d}.")
            
            try:
                response = session.get(url, timeout=10)
                if response.status_code == 404:
                    print(f"😞 No data available for {d}. 😞")
                    continue
                response.raise_for_status()
            except RequestException as e:
                print(f"Network error downloading {d}: {e}")
                continue

            try:
                r = parse_page(response)
                r["date"] = d
                results.append(r)
            except Exception as e:
                print(f"Failed to parse data for {d}: {e}")

            sleep(1.5)
    
    if not results:
        print("No data collected. Can't write CSV.")
        return

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = DictWriter(f, fieldnames=["date"] + COURTS)
        writer.writeheader()
        writer.writerows(results)
        print(f"Successfully saved {len(results)} rows to {out_csv}.")

def main():
    weeks = create_date_list(START_DATE, end_date=WEEKLY_END_DATE, freq="weekly")
    scrape_date_list(weeks, base_url=WEEKLY_URL, out_csv=WEEKLY_CSV)
    months = create_date_list(MONTHLY_START_DATE, freq="monthly")
    scrape_date_list(months, base_url=MONTHLY_URL, out_csv=MONTHLY_CSV)